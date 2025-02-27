from sentence_transformers import SentenceTransformer, util
import faiss
import numpy as np

model = SentenceTransformer('paraphrase-MPNet-base-v2')

def construct_faiss_index(evidence_embeddings):
    d = evidence_embeddings[0].shape[0]
    index = faiss.IndexFlatL2(d)
    index.add(np.array(evidence_embeddings))
    return index

def is_number(token):
    return token.isdigit()

def encode_token(token):
    if is_number(token):
        return token
    return model.encode(token)

def calculate_dynamic_threshold(subject_similarity, object_similarity):
    base_relation_threshold = 0.5
    high_subject_object_similarity = 0.9
    if subject_similarity > high_subject_object_similarity and object_similarity > high_subject_object_similarity:
        # when both subject and object are highly similar, relax the relation threshold
        dynamic_threshold = base_relation_threshold * 0.6
    else:
        dynamic_threshold = base_relation_threshold
    
    return dynamic_threshold

def token_similarity(token1, token2):
    if is_number(token1) or is_number(token2):
        return 1.0 if token1 == token2 else 0.0
    return util.cos_sim(encode_token(token1), encode_token(token2))

def find_contradictions(claim_triples, evidence_triples):
    evidence_embeddings = [model.encode(' '.join(triple)) for triple in evidence_triples]
    index = construct_faiss_index(evidence_embeddings)

    contradictions = []
    for claim in claim_triples:
        claim_str = ' '.join(claim)
        claim_embedding = model.encode(claim_str)
        
        # search for top-N similar triples from evidence
        D, I = index.search(np.array([claim_embedding]), 5)
        for i in I[0]:
            ev_triple = evidence_triples[i]
            
            subject_similarity = token_similarity(claim[0], ev_triple[0])
            relation_similarity = util.cos_sim(model.encode(claim[1]), model.encode(ev_triple[1]))
            print(f"Comparison between {claim[1]} and {ev_triple[1]} is: {relation_similarity}")
            object_similarity = token_similarity(claim[2], ev_triple[2])

            relation_threshold = calculate_dynamic_threshold(subject_similarity, object_similarity)

            if subject_similarity > 0.8 and object_similarity > 0.8 and relation_similarity < relation_threshold:
                contradictions.append({"claim": claim, "evidence": ev_triple, "reason": "relation differs"})

            elif relation_similarity > relation_threshold and object_similarity > 0.8 and subject_similarity < 0.4:
                contradictions.append({"claim": claim, "evidence": ev_triple, "reason": "subject differs"})

            elif subject_similarity > 0.8 and relation_similarity > relation_threshold and object_similarity < 0.4:
                contradictions.append({"claim": claim, "evidence": ev_triple, "reason": "object differs"})
    return contradictions




# # claim = [["apples", "colour", "blue"]]
# # evidence = [["apples", "colour", "red"], ["oranges", "colour", "orange"]]

# claim_kg = [
#     ["eagles", "can", "fly"],
#     ["penguins", "can", "swim"]
# ]

# evidence_kg = [
#     ["eagles", "cannot", "fly"],  # Contradicts the claim about eagles
#     ["penguins", "are good at", "swimming"],  # Similar, but different relation
#     ["ducks", "can", "swim"]
# ]




# print(explain(claim_kg, evidence_kg))