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

def get_capital_of(province):
    wikidata_id = get_wikidata_page_id_from(province)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """SELECT ?item ?itemLabel WHERE {
    wd:%s wdt:P36 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    }"""%(wikidata_id)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    capital = extract_capital_from_results(results)
    
    return capital

def get_wikidata_page_id_from(word):
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json"%(word)
    response = requests.get(url = url).json()['search']

    wikidata_id = extract_wikidataid_from_response(response)

    return wikidata_id

def extract_wikidataid_from_response(response):
    wikidata_id = ''
    for i in response:
        if response_description_valid(i):
            wikidata_id = i['id']
    return wikidata_id

def response_description_valid(response):
    description = r"[Pp]rovince\s(of|in)\s[Ii]ndonesia"
    return 'description' in response and re.search(description, response['description'])

def extract_capital_from_results(results):
    capital = ''
    try:
        capital = results['results']['bindings'][0]['itemLabel']['value']
    except IndexError:
        capital = '-'
    return capital
