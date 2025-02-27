from datasets import load_dataset
if __name__ == "__main__":
    data = load_dataset("potsawee/wiki_bio_gpt3_hallucination", download_mode="force_redownload")['evaluation']

    lengths = []
    consistent = 0
    total = 0

    for i in range(0, 238):
        text = data[i]['gpt3_text']
        claims = data[i]['gpt3_sentences']
        labels = data[i]['annotation']
        
        for sentence in claims:
            lengths.append(len(sentence))

        for label in labels:
            total += 1
            if label == "accurate":
                consistent += 1

    avg_length = sum(lengths) / len(lengths)
    ratio = consistent / total
    
    print(f"Average Len: {avg_length}")
    print(f"ratio: {ratio}")
    print(f"total: {total}")