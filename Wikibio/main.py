from LLM_wb import *
from wikidata_operations import *
from find_relations import *
from comparison_wb import *
from wikipedia_helpers import *
# from triple_contradictions import explain
# from graph_edit_distance import explain_ged

def perform_test(claim_kgs_values, wikidata_relations, labels, j):
    test_results = []

    for i in range(len(labels)):
        curr_label = labels[i]
        curr_claims = claim_kgs_values[i]

        print(f"Claim: {curr_claims}")
        #print(f"Evidence: {wikidata_relations}")

        similarity, kg1_triples, kg2_triples = calculate_similarity(curr_claims, wikidata_relations)
        hallucination_score = 1 - similarity

        # if hallucination_score > 0.5:
        #     explanation = explain_ged(curr_claims, wikidata_relations)
        #     print(f"Explanation: {explanation}")
        #     test_results.append((hallucination_score, curr_label, curr_claims, explanation))
        # else:
        #     test_results.append((hallucination_score, curr_label, curr_claims, None))
        curr_result = [hallucination_score, curr_label, kg1_triples, kg2_triples, j]
        test_results.append(curr_result)
        with open('results_EXTRA_ERRORED.csv', mode='a', newline='') as file:
           writer = csv.writer(file)
           writer.writerow(curr_result)
        print(f"curr test results: \nP(H) = {curr_result[0]}, Label = {curr_result[1]}\nKG1: {curr_result[2]}\nKG2: {curr_result[3]}")
    
    return test_results

def extract_entities_wikidata(text):
    wikidata_NER = wikidata_extract_entities(text)
    wikidata_entities = []
    for entity in wikidata_NER:
        entity_id = "Q" + str(entity.get_id())
        entity_label = entity.get_label()
        wikidata_entities.append([entity_id, entity_label])

    return wikidata_entities

def match_relations_wikidata(wikidata_relations):
    potential_relations = []
    for relation in wikidata_relations:
        entity1 = relation[0][0]
        relation1 = relation[1]
        entity2 = relation[2][0]

        relevant_relations1, list_of_relations_values = retrieve_relations_wikidata(entity1, relation1)
        potential_relations.append([relation[0][1], relevant_relations1, [list_of_relations_values[relation] for relation in relevant_relations1 if relation in list_of_relations_values]])
        relevant_relations2, list_of_relations_values = retrieve_relations_wikidata(entity2, relation1)
        potential_relations.append([relation[2][1], relevant_relations2, [list_of_relations_values[relation] for relation in relevant_relations2 if relation in list_of_relations_values]])

    return [relation for relation in potential_relations if len(relation[0]) > 0 and len(relation[1]) > 0 and len(relation[2]) > 0]

def create_claim_KG(text, claims):
    claim_kgs = construct_kgs(text, claims)
    
    claim_entities = set()
    claim_kgs_values = []

    for sentence, triples in claim_kgs.items():
        processed_triples = [[str(item) for item in triple] for triple in triples]
        claim_kgs_values.append(processed_triples)
        
        for triple in processed_triples:
            claim_entities.add(triple[0])
            claim_entities.add(triple[2])

    return list(claim_entities), claim_kgs_values

entity_description_cache = {}
relation_cache = {}

def get_cached_entity_description(entity):
    if entity in entity_description_cache:
        return entity_description_cache[entity]
    description = retrieve_entity_description_wikidata(entity)
    if description:
        entity_description_cache[entity] = description
    return description

def get_cached_relation(entity1_id, entity2_id):
    if (entity1_id, entity2_id) in relation_cache:
        return relation_cache[(entity1_id, entity2_id)]
    relations = retrieve_relations_wikidata(entity1_id, entity2_id)
    relation_cache[(entity1_id, entity2_id)] = relations
    return relations

def create_wikidata_KG(text, claim_entities):
    wikidata_entities = extract_entities_wikidata(text)
    print(f"---WIKIDATA ENTITIES EXTRACTED---\n{wikidata_entities}\n\n") # 1.5s

    wikidata_relations = []

    searched_entities = set([])
    for entity in wikidata_entities:
        entity_description = get_cached_entity_description(entity[0])
        if entity_description:
          new_ents = construct_kgs_just_text(f"{entity[1]} {entity_description}")["knowledge graph"]
          
          try:
              if isinstance(new_ents, list):
                  wikidata_relations += new_ents
              else:
                  print("Error: new_ents is not in the expected format (list of lists).")
          except (ValueError, SyntaxError) as e:
              print(f"Failed to parse new_ents: {e}")
        else:
            print(f"No description found for {entity[1]}")
        
        for other_entity in wikidata_entities:
            if entity != other_entity:
                curr_relations = get_cached_relation(entity[0], other_entity[0])
                for relation in curr_relations:
                    wikidata_relations.append([entity[1], relation, other_entity[1]])
        
        if entity[0] not in searched_entities:
            relations_entity_link = find_wikipedia_info_entity_link(entity[0])
            searched_entities.add(entity[0])
            if relations_entity_link:
                wikidata_relations += relations_entity_link

    for entity in claim_entities:
      if entity not in searched_entities:
          relations_search = find_wikipedia_info_search(entity)
          searched_entities.add(entity)
          if relations_search != None:
              wikidata_relations += relations_search
    
    return wikidata_relations


import csv
import time
from collections import defaultdict
# print(f"time taken: {time.time() - start}")
import ast
def test(text, claims, labels, i):
    print(f"STARTING TEXT: {text[:50]}\n\n")
    start = time.time()
    test_results = []
    
    # create KG of claim using LLM
    claim_entities, claim_kgs_values = create_claim_KG(text, claims)
    print(f"CREATED ENTITIES, KG: {claim_entities}\n{claim_kgs_values}\n\n")

    # extract wikidata entities matching those in the text
    wikidata_relations = create_wikidata_KG(text, claim_entities)
    print(f"FINAL WIKIDATA KG: \n{wikidata_relations}\n\n")

    test_results = perform_test(claim_kgs_values, wikidata_relations, labels, i)
    
    end = time.time()
    print(f"Time taken: {end - start}s")
    return test_results

from datasets import load_dataset
import random
if __name__ == "__main__":
    #data = load_data()c
    #main(1)
    # claim = '["Malcolm Brogdon (born December 11, 1992) is an American professional basketball player for the Indiana Pacers of the National Basketball Association (NBA).", "He played college basketball for the Virginia Cavaliers, where he was the ACC Player of the Year and an All-American in 2016.", "He was selected in the second round of the 2016 NBA draft by the Milwaukee Bucks with the 36th overall pick.", "Brogdon was named the NBA Rookie of the Year in 2017.", "He was traded to the Pacers in 2019.", "Brogdon is a two-time NBA All-Star and was named to the All-Defensive Second Team in 2019.", "He is known for his defensive prowess and his ability to shoot from long range.", "He is also an advocate for social justice and has been involved in several initiatives to promote racial equality."]'
    # labels = json.loads('["accurate", "accurate", "accurate", "accurate", "accurate", "minor_inaccurate", "accurate", "major_inaccurate"]')
    # test_results = test(claim, labels)
    start_overall = time.time()
    data = load_dataset("potsawee/wiki_bio_gpt3_hallucination", download_mode="force_redownload")['evaluation']

    errored = []
    random_numbers = set([i for i in [11, 34, 36, 48, 77, 82, 92, 93, 138, 187, 203, 229, 230, 231, 232, 233, 234, 235, 236, 237]])
    correct = 0
    total = 0
    for i in random_numbers:
        text = data[i]['gpt3_text']
        claims = data[i]['gpt3_sentences']
        labels = data[i]['annotation']
        try:
            test_results = test(text, claims, labels, i)
            print(f"\n\n---#####---\nFINISHED (i = {i})\n---#####---\n\n")
        except:
            errored.append(i)

    end_overall = time.time()
    print(f"TIME TAKEN: {end_overall - start_overall}s\n")
    print(f"ERRORS: {errored}")

# text = "John Vallely (born April 28, 1947) is an American former professional basketball player. He played in the National Basketball Association (NBA) from 1970 to 1980 as a guard for the Los Angeles Lakers, Atlanta Hawks, and Houston Rockets. Vallely was born in Los Angeles, California. He attended the University of California, Los Angeles (UCLA), where he was a member of the school's 1969–70 NCAA championship team."
# claims = ["John Vallely (born April 28, 1947) is an American former professional basketball player."], ["He played in the National Basketball Association (NBA) from 1970 to 1980 as a guard for the Los Angeles Lakers, Atlanta Hawks, and Houston Rockets."], ["Vallely was born in Los Angeles, California."], ["He attended the University of California, Los Angeles (UCLA), where he was a member of the school's 1969–70 NCAA championship team."]
# labels = ["minor_inaccurate", "minor_inaccurate", "accurate", "accurate"]

# print(test(text, claims, labels))