from SPARQLWrapper import SPARQLWrapper, JSON
import requests

def get_property_label(property_id):
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        'action': 'wbgetentities',
        'ids': property_id,
        'format': 'json',
        'props': 'labels',
        'languages': 'en'
    }
    response = requests.get(url, params=params)
    data = response.json()
    label = data['entities'][property_id]['labels']['en']['value']
    return label

def retrieve_relations_wikidata(entity1_id, entity2_id):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    query = f"""
    SELECT ?statement ?property ?value
    WHERE {{
    wd:{entity1_id} ?property ?value .
    
    FILTER(?value = wd:{entity2_id})
    
    BIND(?property AS ?statement) 
    }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    labels = []

    for result in results["results"]["bindings"]:
        property_uri = result['property']['value']
        property_id = property_uri.split('/')[-1]
        property_label = get_property_label(property_id)
        result['property_label'] = property_label
        labels.append(result['property_label'])
    return labels

def retrieve_entity_description_wikidata(entity):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

    query = f"""
    SELECT ?description WHERE {{
        wd:{entity} schema:description ?description.
        FILTER(LANG(?description) = "en")
    }}
    """

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        description = sparql.query().convert()['results']['bindings'][0]['description']['value']
    except:
        return None
    return description

