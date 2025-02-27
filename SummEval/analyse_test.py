import csv
import numpy as np

import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def obtain_roc():
    y_true = []
    y_scores = []
    
    with open('results_1600.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            p_hall = float(row[0])  # predicted probability
            label = float(row[1])   # true label
            
            y_true.append(0 if label >= 4 else 1)
            y_scores.append(p_hall)
    
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    
    roc_auc = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    plt.title('ROC Curve - SummEval', fontsize=18)
    plt.legend(loc='lower right', fontsize=12)
    plt.show()

obtain_roc()


def obtain_metrics():
    with open('results_1600.csv', newline='') as csvfile:
        results = {}
        for threshold in np.arange(0, 1, 0.05):
            reader = csv.reader(csvfile)
            metrics = {"true_positive": 0, "false_positive": 0, "true_negative": 0, "false_negative": 0}
            correct = 0
            total = 0
            csvfile.seek(0)
            for row in reader:
                total += 1
                p_hall = float(row[0])
                label = float(row[1])

                if label < 4:  # True negative (label < 4)
                    if p_hall < threshold:
                        metrics["false_negative"] += 1
                    else:
                        metrics["true_positive"] += 1
                        correct += 1
                else:  # True positive (label >= 4)
                    if p_hall > threshold:
                        metrics["false_positive"] += 1
                    else:
                        metrics["true_negative"] += 1
                        correct += 1
            
            accuracy = correct / total

            tp = metrics["true_positive"]
            fn = metrics["false_negative"]
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0

            fp = metrics["false_positive"]
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0

            f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

            tn = metrics["true_negative"]
            balanced_accuracy = 0.5 * ((tp / (tp + fn)) + (tn / (tn + fp))) if (tp + fn) > 0 and (tn + fp) > 0 else 0

            results[threshold] = {"accuracy": accuracy, "precision": precision,  "recall": recall, "f1": f1, "balanced_accuracy": balanced_accuracy}
            
            print(f"Threshold: {threshold:.2f}")
            print(f"Accuracy: {accuracy:.4f}")
            print(f"Recall: {recall:.4f}")
            print(f"F1 Score: {f1:.4f}")
            print(f"Balanced Accuracy: {balanced_accuracy:.4f}")
            print("-------------")
        
        max_f1_threshold = max(results, key=lambda t: results[t]["f1"])
        best_f1_result = {max_f1_threshold: results[max_f1_threshold]}
        
        max_balanced_accuracy_threshold = max(results, key=lambda t: results[t]["balanced_accuracy"])
        best_balanced_accuracy_result = {max_balanced_accuracy_threshold: results[max_balanced_accuracy_threshold]}
        
        print("Results for each threshold:")
        print(results)
        
        print("Best threshold for F1 score:")
        print(best_f1_result)
        
        print("Best threshold for Balanced Accuracy:")
        print(best_balanced_accuracy_result)

        

obtain_metrics()

def test_duplicate_kgs():
    with open('results_new.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            kg1 = row[2]
            kg2 = row[3]
            print(kg1 == kg2)

#test_duplicate_kgs()