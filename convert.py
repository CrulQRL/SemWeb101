from rdflib import URIRef, BNode, Literal, Graph, Namespace
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas
import rdflib
import requests
import re

g = Graph()

def extract_luas_hutan():
    data = pandas.read_csv('src/hutan.csv')
    luas = URIRef('http://srabeb.org/type/luas_hutan')

    for _, row in data.iterrows():
        province_name = row['Provinsi']
        province = URIRef('http://srabeb.org/provinsi/' + province_name)

        province_forest_area = row['JumlahLuasDaratandanPerairanKawasanHutan(Ha)']
        forest_area = Literal(province_forest_area)
        
        g.add( (province, luas, forest_area) )


def extract_kelembaban_dan_angin():
    data = pandas.read_csv('src/angin_dan_kelembaban.csv')
    kelembaban = URIRef('http://srabeb.org/type/kelembaban')
    kec_angin = URIRef('http://srabeb.org/type/kecepatan_angin')

    for _, row in data.iterrows():
        province_name = row['Provinsi']
        province = URIRef('http://srabeb.org/provinsi/' + province_name)

        kelembaban_val = row['Kelembaban']
        kelembaban_literal = Literal(kelembaban_val)

        kecepatan_val = row['Kecepatan']
        kecepatan_literal = Literal(kecepatan_val)
        if province:
            g.add( (province, kelembaban, kelembaban_literal) )
            g.add( (province, kec_angin, kecepatan_literal) )
        else:
            print('Provinsi tidak ditemukan: ' + province_name)

def extract_curah_hujan():
    data = pandas.read_csv('src/curah_hujan.csv')
    jumlah_curah_hujan = URIRef('http://srabeb.org/type/curah_hujan')

    for _, row in data.iterrows():
        province_name = row['Provinsi']
        province = URIRef('http://srabeb.org/provinsi/' + province_name)

        curah_hujan_val = row['JumlahCurahHujan']
        curah_hujan_literal = Literal(curah_hujan_val)

        if province:
            g.add( (province, jumlah_curah_hujan, curah_hujan_literal) )
        else:
            print('Provinsi tidak ditemukan: ' + province_name)


extract_luas_hutan()
extract_kelembaban_dan_angin()
extract_curah_hujan()

# n = Namespace('http://srabeb.org/provinsi/')

def get_data_of(province):
    hasil = []
    prov = rdflib.URIRef("http://srabeb.org/provinsi/%s"%province)
    qres = g.query(
        """select ?provinsi ?curah ?hutan ?kelembaban ?kecepatan_angin
        where {
            ?provinsi <http://srabeb.org/type/curah_hujan> ?curah .
            ?provinsi <http://srabeb.org/type/luas_hutan> ?hutan .
            ?provinsi <http://srabeb.org/type/kelembaban> ?kelembaban .
            ?provinsi <http://srabeb.org/type/kecepatan_angin> ?kecepatan_angin .
        }
        """
    , initBindings={'provinsi': prov})
    for row in qres:
        hasil.append("provinsi:%s, curah:%s, hutan:%s, kelembaban:%s, kecepatan_angin:%s" % row)
    return hasil

def get_wikidata_page_id_from(word):
    url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search=%s&language=en&format=json"%(word)
    response = requests.get(url = url).json()['search']

    wikidata_id = get_wikidataid_from_response(response)

    return wikidata_id

def get_wikidataid_from_response(response):
    wikidata_id = ''
    for i in response:
        if response_description_valid(i):
            wikidata_id = i['id']
    return wikidata_id

def response_description_valid(response):
    description = r"[Pp]rovince\s(of|in)\s[Ii]ndonesia"
    return 'description' in response and re.search(description, response['description'])

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

def extract_capital_from_results(results):
    capital = ''
    try:
        capital = results['results']['bindings'][0]['itemLabel']['value']
    except IndexError:
        capital = '-'
    return capital
