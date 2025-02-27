# https://github.com/egerber/spacy-entity-linker
import spacy
import requests

def wikidata_extract_entities(text):
    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe("entityLinker", last=True)

    doc = nlp(text)

    # returns all entities in the whole document
    all_linked_entities = doc._.linkedEntities
    return all_linked_entities

    for sent in doc.sents:
        sent._.linkedEntities.pretty_print()

    '''
    each linked Entity is an object of type EntityElement. Each entity contains the methods

    get_description() returns description from Wikidata
    get_id() returns Wikidata ID
    get_label() returns Wikidata label
    get_span(doc) returns the span from the spacy document that contains the linked entity. You need to provide the current doc as argument, in order to receive an actual spacy.tokens.Span object, otherwise you will receive a SpanInfo emulating the behaviour of a Span
    get_url() returns the url to the corresponding Wikidata item
    pretty_print() prints out information about the entity element
    get_sub_entities(limit=10) returns EntityCollection of all entities that derive from the current entityElement (e.g. fruit -> apple, banana, etc.)
    get_super_entities(limit=10) returns EntityCollection of all entities that the current entityElement derives from (e.g. New England Patriots -> Football Team))
    '''


def wikidata_extract_relations(entity_id):
    url = f'https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json'
    response = requests.get(url)
    data = response.json()

    entity_data = data['entities'][entity_id]
    properties = entity_data['claims']
    print(properties)

    relations = []

    for prop in properties:
        for claim in properties[prop]:
            prop_id = prop
            value = claim['mainsnak']['datavalue']['value']
            prop_label = requests.get(f'https://www.wikidata.org/wiki/Special:EntityData/{prop_id}.json').json()
            prop_label = prop_label['entities'][prop_id]['labels']['en']['value']
            relations.append((prop_label, value))
    
    return relations


