import networkx as nx
from networkx.algorithms.similarity import graph_edit_distance
from llm import explain_ged_operations

def list_to_graph(edges):
    G = nx.DiGraph()
    for edge in edges:
        try:
            src, rel, dst = edge
            G.add_edge(src, dst, relation=rel)
        except:
            continue
    return G

def get_edit_operations(G1, G2):
    operations = []
    
    for node in G1.nodes:
        if node not in G2.nodes:
            pass
            #operations.append(f"Delete node {node} from G1")
            #operations.append((f"DN", f"{node}"))
    
    for node in G2.nodes:
        if node not in G1.nodes:
            pass
            #operations.append(f"Add node {node} to G1")
            #operations.append((f"AN", f"{node}"))
    
    for u, v, data in G1.edges(data=True):
        if not G2.has_edge(u, v) or G2.get_edge_data(u, v) != data:
            #operations.append(f"Delete edge ({u}, {v}) with attributes {data} from G1")
            operations.append((f"DE", f"{u}", f"{v}", f"{data['relation']}"))
    
    for u, v, data in G2.edges(data=True):
        if not G1.has_edge(u, v) or G1.get_edge_data(u, v) != data:
            #operations.append(f"Add edge ({u}, {v}) with attributes {data} to G1")
            operations.append((f"AE", f"{u}", f"{v}", f"{data['relation']}"))
    
    return operations

def generate_explanations(operations):
    explanations = []
    
    for op in operations:
        if op[0] == 'DN':  # Delete Node
            explanations.append(f"The entity '{op[1]}' is present in the hallucinated response but does not exist in the factual knowledge base.")
        elif op[0] == 'AN':  # Add Node
            explanations.append(f"The entity '{op[1]}' is missing in the hallucinated response but exists in the factual knowledge base.")
        elif op[0] == 'DE':  # Delete Edge
            explanations.append(f"The relationship '{op[3]}' between '{op[1]}' and '{op[2]}' is present in the hallucinated response but does not exist in the factual knowledge base.")
        elif op[0] == 'AE':  # Add Edge
            explanations.append(f"The relationship '{op[3]}' between '{op[1]}' and '{op[2]}' is missing in the hallucinated response but exists in the factual knowledge base.")
    
    return explanations

def explain_ged(summary, context, contradictory_claims, contradictory_evidences):
    # G_claim = list_to_graph(kg1)
    # G_evidence = list_to_graph(kg2)
    # operations = get_edit_operations(G_claim, G_evidence)
    G_claim_contradictory = list_to_graph(contradictory_claims)
    G_evidence_contradictory = list_to_graph(contradictory_evidences)
    operations_contradictory = get_edit_operations(G_claim_contradictory, G_evidence_contradictory)
    #operations += operations_contradictory
    explanation = generate_explanations(operations_contradictory)
    return explain_ged_operations(summary, context, explanation)





claim = [
    ["Donald Trump", "painted", "Mona Lisa"],
    ["Leonardo da Vinci", "was a", "Astronaut"],
    ["Vincent van Gogh", "painted", "Starry Night"],
    ["Vincent van Gogh", "was a", "Impressionist"]
]

evidence = [
    ["Leonardo da Vinci", "painted", "Mona Lisa"],
    ["Leonardo da Vinci", "was a", "Renaissance Artist"],
    ["Vincent van Gogh", "painted", "Starry Night"],
    ["Vincent van Gogh", "was a", "Impressionist"]
]

#print(explain_ged(claim, evidence))