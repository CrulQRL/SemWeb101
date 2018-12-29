from SPARQLWrapper import SPARQLWrapper, JSON
from graph_query import (
    add_provinces_capital_to_graph,
    add_provinces_map_to_graph)
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
    }""" % (wikidata_id)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    province_map = extract_itemlabel_from_query_result(results)
    add_provinces_map_to_graph(province, province_map)

    return province_map


def get_capital_of(province):
    wikidata_id = get_province_wikidata_id(province)

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    query = """SELECT ?item ?itemLabel WHERE {
    wd:%s wdt:P36 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    }""" % (wikidata_id)

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    capital = extract_itemlabel_from_query_result(results)
    add_provinces_capital_to_graph(province, capital)

    if capital == '-':
        return 'Jakarta'
    return capital


def get_province_wikidata_id(province):
    url = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json' % (province)
    response = requests.get(url=url).json()['search']

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


def get_provinces_capital_data(province):
    wikidata_id = get_province_wikidata_id(province)

    query = """SELECT ?areaLabel ?elevation_above_sea_levelLabel ?located_in_time_zoneLabel ?locator_map_imageLabel ?populationLabel WHERE {
    wd:%s wdt:P36 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    OPTIONAL { ?item wdt:P2046 ?area. }
    OPTIONAL { ?item wdt:P2044 ?elevation_above_sea_level. }
    OPTIONAL { ?item wdt:P1082 ?population. }
    OPTIONAL { ?item wdt:P242 ?locator_map_image. }
    OPTIONAL { ?item wdt:P421 ?located_in_time_zone. }
    }""" % (wikidata_id)

    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return check_null_value_in_(results["results"]["bindings"][0])


def check_null_value_in_(result):
    expected_result_keys = [
        'areaLabel',
        'elevation_above_sea_levelLabel',
        'located_in_time_zoneLabel',
        'locator_map_imageLabel',
        'populationLabel'
    ]

    for i in expected_result_keys:
        if i not in result:
            result[i] = {'type': '-', 'value': '-'}

    return result


def get_data_capital_of_indonesia():
    query = """SELECT ?areaLabel ?elevation_above_sea_levelLabel ?located_in_time_zoneLabel ?locator_map_imageLabel ?populationLabel WHERE {
    wd:Q252 wdt:P36 ?item.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "id". }
    OPTIONAL { ?item wdt:P2046 ?area. }
    OPTIONAL { ?item wdt:P2044 ?elevation_above_sea_level. }
    OPTIONAL { ?item wdt:P1082 ?population. }
    OPTIONAL { ?item wdt:P242 ?locator_map_image. }
    OPTIONAL { ?item wdt:P421 ?located_in_time_zone. }
    }
    LIMIT 1"""
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results["results"]["bindings"][0]
