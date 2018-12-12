from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import re

def get_list_of_provinces():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""SELECT ?item ?itemLabel WHERE {
    ?item wdt:P31 wd:Q5098.
    SERVICE wikibase:label {bd:serviceParam wikibase:language "id" .}
    }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results

def get_map(province):
    wikidata_id = get_province_wikidata_id(province)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """SELECT ?item ?itemLabel WHERE {
    wd:%s wdt:P242 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    }"""%(wikidata_id)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    province_map = extract_itemlabel_from_query_result(results)
    
    return province_map

def get_capital_of(province):
    wikidata_id = get_province_wikidata_id(province)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """SELECT ?item ?itemLabel WHERE {
    wd:%s wdt:P36 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    }"""%(wikidata_id)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    capital = extract_itemlabel_from_query_result(results)
    
    return capital

def get_province_wikidata_id(province):
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json"%(province)
    response = requests.get(url = url).json()['search']

    wikidata_id = extract_province_id_from(response)

    return wikidata_id

def extract_province_id_from(response):
    wikidata_id = ''
    for i in response:
        if response_description_contains_province(i):
            wikidata_id = i['id']
    return wikidata_id

def response_description_contains_province(response):
    description = r"[Pp]rovince\s(of|in)\s[Ii]ndonesia"
    return 'description' in response and re.search(description, response['description'])

def extract_itemlabel_from_query_result(results):
    item_label_value = ''
    try:
        item_label_value = results['results']['bindings'][0]['itemLabel']['value']
    except IndexError:
        item_label_value = '-'
    return item_label_value
