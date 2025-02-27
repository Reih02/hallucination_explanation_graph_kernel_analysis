import csv
import ast
from ged import explain_ged
from find_contradictions import find_contradictions
from llm import *
from comparison import *

def run_test_individual(summary, context, consistency):
    duplicate = True
    tries = 0
    # while duplicate:
    tries += 1
    output = final_kg_constructor(summary, context)
    KGs = json.loads(output)

    claim_kg = KGs["knowledge_graph1"]
    context_kg = KGs["knowledge_graph2"]

    #print(f"claim: {type(claim_kg[0])}")
    #return
        # if check_kgs_valid(claim_kg, context_kg):
        #     duplicate = False
        #     if tries >= 10:
        #         print("CANT CREATE KGS")
        #         return
        #     break

    print(f"### CLAIM ###:\n{claim_kg}\n\n### CONTEXT ###:\n{context_kg}")

    similarity, kg1, kg2 = calculate_similarity(claim_kg, context_kg)

    if consistency <= 3:
        contradictions = find_contradictions(claim_kg, context_kg)
        print(f"CONTRADICTIONS: {contradictions}")
        if len(contradictions) > 0:
            contradictory_claims = []
            contradictory_evidence = []
            for contradiction in contradictions:
                contradictory_claims.append(contradiction['claim'])
                contradictory_evidence.append(contradiction['evidence'])
            explanation = explain_ged(summary, context, contradictory_claims, contradictory_evidence)
            print(f"###EXPLANATION###: \n{explanation}\n\n###############")
        else:
            explanation = explain_ged(summary, context, claim_kg, context_kg)
            print(f"###EXPLANATION###: \n{explanation}\n\n###############")

        

    print(f"SIMILARITY: {similarity} | LABEL: {consistency}\n\nKG1_RELABELLED: {kg1}\n\nKG2_RELABELLED: {kg2}")


summary =  "Rome is the capital city of France. France is a country in Asia. France has 900 million occupants. France shares a border with Germany."
context = "Paris is the capital city of France. France is a country in Europe. France has 66.6 million occupants. France shares a border with Germany "
run_test_individual(summary, context, 2)

# summary = "russian fighter jet intercepted a u.s. reconnaissance plane in an `` unsafe '' manner '' . pentagon says the incident occurred in international airspace north of poland . the russian jet flew within 100 feet of a rc-135u over the baltic sea of okhotsk in the western pacific . it was intercepted by a russian su-27 flanker . the united states is complaining about incident involving the incident ."
# context = "(CNN)After a Russian fighter jet intercepted a U.S. reconnaissance plane in an 'unsafe and unprofessional manner' earlier this week, the United States is complaining to Moscow about the incident. On Tuesday, a U.S. RC-135U was flying over the Baltic Sea when it was intercepted by a Russian SU-27 Flanker. The Pentagon said the incident occurred in international airspace north of Poland. The U.S. crew believed the Russian pilot's actions were 'unsafe and unprofessional due to the aggressive maneuvers it performed in close proximity to their aircraft and its high rate of speed,' Pentagon spokesman Mark Wright said. Russian state news agency Sputnik reported the U.S. plane was flying toward the Russian border with its transponder switched off, according to a Defense Ministry spokesman. Maj. Gen. Igor Konashenkov said the Russian jet flew around the U.S. plane several times to identify it and get its tail number. An official with the U.S. European Command said the claim that the transponder was off was false. Wright said the Pentagon and State Department will 'file the appropriate petition through diplomatic channels' with Russia. This is not the first time the U.S. has complained about an incident involving a RC-135U and a SU-27. A year ago, a Russian jet flew within 100 feet of a RC-135U over the Sea of Okhotsk in the western Pacific, according to U.S. officials who called it 'one of the most dangerous close passes in decades.' The Pentagon complained to the Russia military about that incident. Russian and U.S. aircraft often encounter each other, both in Northern Europe as well as the area between the Russian Far East and Alaska. CNN's Steve Brusk and Jamie Crawford contributed to this report."
# run_test_individual(summary, context, 5.0)

# with open('results_big.csv', newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         i = 0
#         for row in reader:
#             if i > 0:
#                 break

#             hallucination_score = float(row[0])
#             label = row[1]

#             row_2 = ast.literal_eval(row[2])
#             kg1 = [
#                 [subject, details['relation'], object_] 
#                 for subject, object_, details in row_2
#             ]
#             row_3 = ast.literal_eval(row[3])
#             kg2 = [
#                 [subject, details['relation'], object_] 
#                 for subject, object_, details in row_3
#             ]

#             if hallucination_score > 0.9 and label == "major_inaccurate":
#                 i += 1
#                 contradictions = find_contradictions(kg1, kg2)
#                 print(contradictions)
#                 print(f"###----------------###\nKG1: {kg1}\nKG2: {kg2}\n\n")
#                 explanation = explain_ged(kg1, kg2)
#                 print(f"Explanation: {explanation}\n###----------------###\n\n\n")

# def test_explanation(KG1, KG2):
#     kg1 = [
#         [subject, details['relation'], object_] 
#         for (subject, object_, details) in KG1
#     ]
#     kg2 = [
#         [subject, details['relation'], object_] 
#         for (subject, object_, details) in KG2
#     ]

#     contradictions = find_contradictions(kg1, kg2)
    
#     print(f"###----------------###\nContradicting triples: {contradictions}\n\nKG1: {kg1}\nKG2: {kg2}\n\n")
#     explanation = explain_ged(kg1, kg2)
#     print(f"Explanation: {explanation}\n###----------------###\n\n\n")

# KG1 = "[('john russell reynolds', '1820', {'relation': 'born'}), ('john russell reynolds', '1876', {'relation': 'died'}), ('john russell reynolds', 'english', {'relation': 'nationality'}), ('john russell reynolds', 'lawyer', {'relation': 'occupation'}), ('john russell reynolds', 'judge', {'relation': 'occupation'}), ('john russell reynolds', 'author', {'relation': 'occupation'})]"
# KG2 = "[('john russell reynolds', '1828', {'relation': 'born'}), ('john russell reynolds', '1896', {'relation': 'died'}), ('john russell reynolds', 'english', {'relation': 'nationality'}), ('john russell reynolds', 'physician', {'relation': 'occupation'}), ('judge', 'law', {'relation': 'field of this occupation'})]"
# test_explanation(KG1, KG2)