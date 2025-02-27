import csv
import ast
import time
from comparison_QAGS import *
from LLM_QAGS import *
import re
import json

def run_test(summary, context, hallucination):
    # print(f"\n\nSummary: {summary}\nContext: {context[:50]}\nHallucination: {hallucination}")
    # print(len(summary), len(hallucination))
    for i in range(len(summary)):
        output = final_kg_constructor(summary[i], context)
        KGs = json.loads(output)

        claim_kg = KGs["knowledge_graph1"]
        context_kg = KGs["knowledge_graph2"]

        print(f"### CLAIM ###:\n{claim_kg}\n\n### CONTEXT ###:\n{context_kg}")

        similarity, kg1, kg2 = calculate_similarity(claim_kg, context_kg)

        print(f"SIMILARITY: {similarity} | LABEL: {hallucination[i]}\n\nKG1_RELABELLED: {kg1}\n\nKG2_RELABELLED: {kg2}")

        curr_consistency = hallucination[i]
        hallucination_score = 1 - similarity

        #print(f"Hallucination score: {hallucination_score}\nConsistency: {curr_consistency}")

        curr_result = [hallucination_score, curr_consistency, kg1, kg2]
        with open('results_2.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(curr_result)
        print(f"curr test results: \nP(H) = {curr_result[0]}, Label = {curr_result[1]}")


if __name__ == "__main__":
    filename = "mturk_cnndm.jsonl"
    errors = []

    with open(filename, 'r') as file:
        i = 0
        for line in file:
            i += 1
            if i <= 50:
                continue
            try:
                row = json.loads(line)

                article = row.get("article", "")

                summary_sentences = row.get("summary_sentences", [])
                sentences = [entry["sentence"] for entry in summary_sentences]
                responses = [entry["responses"] for entry in summary_sentences]

                    
                for response in responses:
                    average_labels = []
                    for nested_list in responses:
                        scores = [1 if item['response'] == 'yes' else 0 for item in nested_list]
                        average = sum(scores) / len(scores)
                        average_labels.append(average)

                run_test(sentences, article, average_labels)
            except Exception as e:
                errors.append((line, e))
                print("Error occured")
                continue
    print(errors)