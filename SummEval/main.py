from datasets import load_dataset
import csv
import ast
import time
from comparison_se import *
from LLM_se import *
import re
import json

def check_kgs_valid(kg1, kg2):
    for graph in [kg1, kg2]:
        if not all(len(triple) == 3 for triple in graph):
            return False
        
    claim_entity_pairs = {(triple[0], triple[2]) for triple in kg1}
    context_entity_pairs = {(triple[0], triple[2]) for triple in kg2}

    if claim_entity_pairs == context_entity_pairs:
        return False

    return True


def run_test_individual(summary, context, consistency):
    duplicate = True
    tries = 0
    # while duplicate:
    tries += 1
    output = final_kg_constructor(summary, context)
    KGs = json.loads(output)

    claim_kg = KGs["knowledge_graph1"]
    context_kg = KGs["knowledge_graph2"]

        # if check_kgs_valid(claim_kg, context_kg):
        #     duplicate = False
        #     if tries >= 10:
        #         print("CANT CREATE KGS")
        #         return
        #     break

    print(f"### CLAIM ###:\n{claim_kg}\n\n### CONTEXT ###:\n{context_kg}")

    similarity, kg1, kg2 = calculate_similarity(claim_kg, context_kg)

    print(f"SIMILARITY: {similarity} | LABEL: {consistency}\n\nKG1_RELABELLED: {kg1}\n\nKG2_RELABELLED: {kg2}")

# summary = "russian fighter jet intercepted a u.s. reconnaissance plane in an `` unsafe '' manner '' . pentagon says the incident occurred in international airspace north of poland . the russian jet flew within 100 feet of a rc-135u over the baltic sea of okhotsk in the western pacific . it was intercepted by a russian su-27 flanker . the united states is complaining about incident involving the incident ."
# context = "(CNN)After a Russian fighter jet intercepted a U.S. reconnaissance plane in an 'unsafe and unprofessional manner' earlier this week, the United States is complaining to Moscow about the incident. On Tuesday, a U.S. RC-135U was flying over the Baltic Sea when it was intercepted by a Russian SU-27 Flanker. The Pentagon said the incident occurred in international airspace north of Poland. The U.S. crew believed the Russian pilot's actions were 'unsafe and unprofessional due to the aggressive maneuvers it performed in close proximity to their aircraft and its high rate of speed,' Pentagon spokesman Mark Wright said. Russian state news agency Sputnik reported the U.S. plane was flying toward the Russian border with its transponder switched off, according to a Defense Ministry spokesman. Maj. Gen. Igor Konashenkov said the Russian jet flew around the U.S. plane several times to identify it and get its tail number. An official with the U.S. European Command said the claim that the transponder was off was false. Wright said the Pentagon and State Department will 'file the appropriate petition through diplomatic channels' with Russia. This is not the first time the U.S. has complained about an incident involving a RC-135U and a SU-27. A year ago, a Russian jet flew within 100 feet of a RC-135U over the Sea of Okhotsk in the western Pacific, according to U.S. officials who called it 'one of the most dangerous close passes in decades.' The Pentagon complained to the Russia military about that incident. Russian and U.S. aircraft often encounter each other, both in Northern Europe as well as the area between the Russian Far East and Alaska. CNN's Steve Brusk and Jamie Crawford contributed to this report."
# run_test_individual(summary, context, 5.0)

# text1 = "tim durkan photographed aerial shots of the sunset warming the city 's skyline and shared them on cnn ireport . the fires were started in southeastern siberia , by farmers burning grass in their fields . the flames quickly grew out of control because of strong winds and spread throughout the region ."
# text2 = "(CNN)A fiery sunset greeted people in Washington Sunday. The deep reddish color caught Seattle native Tim Durkan's eye. He photographed a handful of aerial shots of the sunset warming the city's skyline and shared them on CNN iReport. The stunning sunsets were the result of raging wildfires in parts of Siberia. \"The dramatic sunsets began showing up over the weekend and had Seattle locals wondering where the amber-colored haze was originating from,\" Durken said. The fires were started in southeastern Siberia, by farmers burning grass in their fields. But on April 14, it is believed that the flames quickly grew out of control because of strong winds and spread throughout the region, according to CNN affiliate KOMO-TV. As a result, the fires have destroyed dozens of villages in the region. Rescue crews were able to put out the flames. However, the lingering smoke from the widespread fires were picked up by atmospheric winds. The winds carried the smoke from Siberia across the Pacific Ocean and brought it to the Pacific Northwest. Parts of Oregon, Washington and British Columbia are seeing the results of the smoke, wind and solar light combination. The reason people are seeing an intense red sunset is a result of smoke particles filtering out the shorter wavelength colors from the sunlight like greens, blues, yellows and purples, KOMO-TV said. That means colors like red and orange are able to penetrate the air unfiltered. The colors are especially intense during sunrises and sunsets because there is more atmosphere for the light to travel through to get to a person's eye. As the smoke starts to dissipate, air quality will get better and these fiery sunsets will lose their reddish hue."
# run_test_individual(text1, text2, 5)

# summary = "donald sterling , nba team last year . sterling 's wife sued for $ 2.6 million in gifts . sterling says he is the former female companion who has lost the . sterling has ordered v. stiviano to pay back $ 2.6 m in gifts after his wife sued . sterling also includes a $ 391 easter bunny costume , $ 299 and a $ 299 ."
# context = "(CNN)Donald Sterling's racist remarks cost him an NBA team last year. But now it's his former female companion who has lost big. A Los Angeles judge has ordered V. Stiviano to pay back more than $2.6 million in gifts after Sterling's wife sued her. In the lawsuit, Rochelle 'Shelly' Sterling accused Stiviano of targeting extremely wealthy older men. She claimed Donald Sterling used the couple's money to buy Stiviano a Ferrari, two Bentleys and a Range Rover, and that he helped her get a $1.8 million duplex. Who is V. Stiviano? Stiviano countered that there was nothing wrong with Donald Sterling giving her gifts and that she never took advantage of the former Los Angeles Clippers owner, who made much of his fortune in real estate. Shelly Sterling was thrilled with the court decision Tuesday, her lawyer told CNN affiliate KABC. 'This is a victory for the Sterling family in recovering the $2,630,000 that Donald lavished on a conniving mistress,' attorney Pierce O'Donnell said in a statement. 'It also sets a precedent that the injured spouse can recover damages from the recipient of these ill-begotten gifts.' Stiviano's gifts from Donald Sterling didn't just include uber-expensive items like luxury cars. According to the Los Angeles Times, the list also includes a $391 Easter bunny costume, a $299 two-speed blender and a $12 lace thong. Donald Sterling's downfall came after an audio recording surfaced of the octogenarian arguing with Stiviano. In the tape, Sterling chastises Stiviano for posting pictures on social media of her posing with African-Americans, including basketball legend Magic Johnson. 'In your lousy f**ing Instagrams, you don't have to have yourself with -- walking with black people,' Sterling said in the audio first posted by TMZ. He also tells Stiviano not to bring Johnson to Clippers games and not to post photos with the Hall of Famer so Sterling's friends can see. 'Admire him, bring him here, feed him, f**k him, but don't put (Magic) on an Instagram for the world to have to see so they have to call me,' Sterling said. NBA Commissioner Adam Silver banned Sterling from the league, fined him $2.5 million and pushed through a charge to terminate all of his ownership rights in the franchise. Fact check: Donald Sterling's claims vs. reality CNN's Dottie Evans contributed to this report."
# run_test_individual(summary, context, 1.67)



def run_test(summary, context, consistency):
    for i in range(len(consistency)):
        output = final_kg_constructor(summary[i], context)
        KGs = json.loads(output)

        claim_kg = KGs["knowledge_graph1"]
        context_kg = KGs["knowledge_graph2"]

        print(f"### CLAIM ###:\n{claim_kg}\n\n### CONTEXT ###:\n{context_kg}")

        similarity, kg1, kg2 = calculate_similarity(claim_kg, context_kg)

        print(f"SIMILARITY: {similarity} | LABEL: {consistency}\n\nKG1_RELABELLED: {kg1}\n\nKG2_RELABELLED: {kg2}")

        curr_consistency = consistency[i]
        hallucination_score = 1 - similarity

        #print(f"Hallucination score: {hallucination_score}\nConsistency: {curr_consistency}")

        curr_result = [hallucination_score, curr_consistency, kg1, kg2]
        with open('results_1600.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(curr_result)
        print(f"curr test results: \nP(H) = {curr_result[0]}, Label = {curr_result[1]}")

    
import time
if __name__ == "__main__":
    data = load_dataset("mteb/summeval")["test"]
    errors = []
    start = time.time()
    for i in range(34, 45):
        try:
            curr_id = data[i]['id']
            curr_summary = data[i]['machine_summaries']
            curr_context = data[i]['text']
            curr_consistency = data[i]['consistency']
            run_test(curr_summary, curr_context, curr_consistency)
        except Exception as e:
            errors.append((i, e))
            print("Error occured")
            continue
    print(errors)
    end = time.time()
    print(f"Time taken: {end - start}s")