# import json

# def parse_file(file_path):
#     with open(file_path, 'r', encoding='utf-8') as file:
#         content = file.read()

#     entries = content.split("-------------------------------------------------------------------------------------------------------------------------")
    
#     parsed_data = []
#     for entry in entries:
#         if entry.strip():
#             data = {}
#             lines = entry.strip().split("\n")
#             key = None
#             value = []
            
#             for line in lines:
#                 line = line.strip()
#                 if line.startswith("###") and (line.endswith("###:") or line.endswith("###: ") or line.endswith(":###") or line.endswith(":### ")):
#                     if key:
#                         data[key] = "\n".join(value).strip()
                    
#                     key = line.replace("###", "").replace(":", "").strip().lower()
#                     value = []
#                 elif key:
#                     value.append(line)
            
#             if key:
#                 data[key] = "\n".join(value).strip()
            
#             parsed_data.append(data)
    
#     return parsed_data

# def save_as_json(parsed_data, output_path):
#     with open(output_path, 'w', encoding='utf-8') as json_file:
#         json.dump(parsed_data, json_file, indent=4)

# file_path = 'explanation_analysis.txt'
# output_path = 'parsed_test.json'

# parsed_data = parse_file(file_path)
# save_as_json(parsed_data, output_path)

# print(f"Parsed data saved to {output_path}")

# from collections import defaultdict

# with open("parsed_test.json", "r") as file:
#     data = json.load(file)

# total_detail = 0
# total_completeness = 0
# total_accuracy_reliability = 0
# total_trustworthiness = 0

# groups = defaultdict(list)

# for entry in data:
#     consistency = float(entry["consistency"])
#     if 0 <= consistency <= 1:
#         groups["0-1"].append(entry)
#     elif 1 < consistency <= 2:
#         groups["1-2"].append(entry)
#     elif 2 < consistency <= 3:
#         groups["2-3"].append(entry)

#     total_detail += int(entry["detail"])
#     total_completeness += int(entry["completeness"])
#     total_accuracy_reliability += int(entry["accuracy and reliability"])
#     total_trustworthiness += int(entry["trustworthiness"])

# num_entries = len(data)
# overall_avg_detail = total_detail / num_entries
# overall_avg_completeness = total_completeness / num_entries
# overall_avg_accuracy_reliability = total_accuracy_reliability / num_entries
# overall_avg_trustworthiness = total_trustworthiness / num_entries

# group_averages = {}
# for group, entries in groups.items():
#     group_total_detail = sum(int(entry["detail"]) for entry in entries)
#     group_total_completeness = sum(int(entry["completeness"]) for entry in entries)
#     group_total_accuracy_reliability = sum(int(entry["accuracy and reliability"]) for entry in entries)
#     group_total_trustworthiness = sum(int(entry["trustworthiness"]) for entry in entries)
#     num_group_entries = len(entries)
    
#     group_averages[group] = {
#         "avg_detail": group_total_detail / num_group_entries,
#         "avg_completeness": group_total_completeness / num_group_entries,
#         "avg_accuracy_reliability": group_total_accuracy_reliability / num_group_entries,
#         "avg_trustworthiness": group_total_trustworthiness / num_group_entries,
#     }

# print("Overall Averages:")
# print(f"Detail: {overall_avg_detail:.2f}")
# print(f"Completeness: {overall_avg_completeness:.2f}")
# print(f"Accuracy and Reliability: {overall_avg_accuracy_reliability:.2f}")
# print(f"Trustworthiness: {overall_avg_trustworthiness:.2f}")
# print()

# print("Group Averages:")
# for group, averages in group_averages.items():
#     print(f"Group {group}:")
#     print(f"  Detail: {averages['avg_detail']:.2f}")
#     print(f"  Completeness: {averages['avg_completeness']:.2f}")
#     print(f"  Accuracy and Reliability: {averages['avg_accuracy_reliability']:.2f}")
#     print(f"  Trustworthiness: {averages['avg_trustworthiness']:.2f}")
#     print()




import json
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def parse_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    entries = content.split("-------------------------------------------------------------------------------------------------------------------------")
    
    parsed_data = []
    for entry in entries:
        if entry.strip():
            data = {}
            lines = entry.strip().split("\n")
            key = None
            value = []
            
            for line in lines:
                line = line.strip()
                if line.startswith("###") and (line.endswith("###:") or line.endswith("###: ") or line.endswith(":###") or line.endswith(":### ")):
                    if key:
                        data[key] = "\n".join(value).strip()
                    
                    key = line.replace("###", "").replace(":", "").strip().lower()
                    value = []
                elif key:
                    value.append(line)
            
            if key:
                data[key] = "\n".join(value).strip()
            
            parsed_data.append(data)
    
    return parsed_data

def save_as_json(parsed_data, output_path):
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(parsed_data, json_file, indent=4)

file_path = 'explanation_analysis.txt'
output_path = 'parsed_test.json'

parsed_data = parse_file(file_path)
save_as_json(parsed_data, output_path)

print(f"Parsed data saved to {output_path}")

with open("parsed_test.json", "r") as file:
    data = json.load(file)

groups = defaultdict(list)
overall_metrics = {"detail": 0, "completeness": 0, "accuracy and reliability": 0, "trustworthiness": 0}

for entry in data:
    consistency = float(entry["consistency"])
    if 0 <= consistency <= 1:
        groups["0-1"].append(entry)
    elif 1 < consistency <= 2:
        groups["1-2"].append(entry)
    elif 2 < consistency <= 3:
        groups["2-3"].append(entry)

    overall_metrics["detail"] += int(entry["detail"])
    overall_metrics["completeness"] += int(entry["completeness"])
    overall_metrics["accuracy and reliability"] += int(entry["accuracy and reliability"])
    overall_metrics["trustworthiness"] += int(entry["trustworthiness"])

num_entries = len(data)
overall_avg_metrics = {key: value / num_entries for key, value in overall_metrics.items()}

group_averages = {}
for group, entries in groups.items():
    group_metrics = {"detail": 0, "completeness": 0, "accuracy and reliability": 0, "trustworthiness": 0}
    for entry in entries:
        group_metrics["detail"] += int(entry["detail"])
        group_metrics["completeness"] += int(entry["completeness"])
        group_metrics["accuracy and reliability"] += int(entry["accuracy and reliability"])
        group_metrics["trustworthiness"] += int(entry["trustworthiness"])
    num_group_entries = len(entries)
    group_averages[group] = {key: value / num_group_entries for key, value in group_metrics.items()}

print("Overall Averages:")
for key, value in overall_avg_metrics.items():
    print(f"{key.capitalize()}: {value:.2f}")

print("\nGroup Averages:")
for group, averages in group_averages.items():
    print(f"Group {group}:")
    for key, value in averages.items():
        print(f"  {key.capitalize()}: {value:.2f}")
    print()

def plot_bar_chart(group, averages):
    labels = list(averages.keys())
    values = list(averages.values())

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'orange', 'red'])
    plt.title(f"Bar Chart for Group {group}")
    plt.ylabel("Average Score")
    plt.ylim(0, 5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_radar_chart(group, averages):
    labels = list(averages.keys())
    values = list(averages.values())
    values += values[:1]

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], fontsize=14)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=22)

    plt.title(f"Radar Chart for Group {group}", fontsize=18)
    plt.tight_layout()
    plt.show()

for group, averages in group_averages.items():
    plot_radar_chart(group, averages)

group_overall_averages = {
    group: np.mean(list(averages.values())) for group, averages in group_averages.items()
}

def plot_group_overall_bar_chart(group_overall_averages):
    sorted_groups = sorted(group_overall_averages.keys(), key=lambda x: float(x.split("-")[0]))
    sorted_overall_averages = [group_overall_averages[group] for group in sorted_groups]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(sorted_groups, sorted_overall_averages, color=['blue', 'orange', 'red'])
    plt.title("Overall Average Scores by Group")
    plt.ylabel("Overall Average")
    plt.ylim(0, 5)
    plt.xticks(rotation=45)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height - 0.2, f'{height:.2f}', ha='center', color='white', fontsize=10)

    plt.tight_layout()
    plt.show()

plot_group_overall_bar_chart(group_overall_averages)
