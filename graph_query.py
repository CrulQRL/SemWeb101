from rdflib import URIRef, Literal
from convert import g
import rdflib


def get_province_statistics(province):
    hasil = ''
    prov = rdflib.URIRef("http://srabeb.org/provinsi/%s" % province)
    qres = g.query(
        """select ?provinsi ?curah ?hutan ?kelembaban ?kecepatan_angin
        where {
            ?provinsi <http://srabeb.org/type/curah_hujan> ?curah .
            ?provinsi <http://srabeb.org/type/luas_hutan> ?hutan .
            ?provinsi <http://srabeb.org/type/kelembaban> ?kelembaban .
            ?provinsi <http://srabeb.org/type/kecepatan_angin> ?kecepatan_angin .
        }
        """, initBindings={'provinsi': prov})

    for row in qres:
        hasil = "provinsi:%s, curah:%s, hutan:%s, kelembaban:%s, kecepatan_angin:%s" % row
    return hasil


def get_province_area_and_island_info(province):
    hasil = ''
    prov = rdflib.URIRef("http://srabeb.org/provinsi/%s" % province)
    qres = g.query(
        """select ?provinsi ?luas ?pulau ?presentase
        where {
            ?provinsi <http://srabeb.org/type/luas> ?luas .
            ?provinsi <http://srabeb.org/type/pulau> ?pulau .
            ?provinsi <http://srabeb.org/type/presentase_luas> ?presentase .
        }
        """, initBindings={'provinsi': prov})

    for row in qres:
        hasil = "provinsi:%s, luas:%s, pulau:%s, presentase_luas:%s" % row

    return hasil 


def get_province_description(province):
    prov = rdflib.URIRef("http://srabeb.org/provinsi/%s" % province)
    qres = g.query(
        """
        select ?desc
        where {
            ?provinsi <http://srabeb.org/type/deskripsi> ?desc .
        }
        """, initBindings={'provinsi': prov})

    hasil = ''
    for row in qres:
        hasil = 'deskripsi:%s' % row

    return hasil


def insert_province_description(province, description):
    prov = URIRef('http://srabeb.org/provinsi/' + province)
    deskripsi = URIRef('http://srabeb.org/type/deskripsi')
    deskripsi_literal = Literal(description)

    g.add((prov, deskripsi, deskripsi_literal))


def add_provinces_capital_to_graph(province, capital):
    prov = URIRef('http://srabeb.org/provinsi/' + province)
    has_capital = URIRef('http://srabeb.org/type/has_capital')
    capital = URIRef('http://srabeb.org/capital/' + capital)

    g.add((prov, has_capital, capital))


def add_provinces_map_to_graph(province, map):
    prov = URIRef('http://srabeb.org/provinsi/' + province)
    has_map = URIRef('http://srabeb.org/type/has_map')
    map_image = URIRef('http://srabeb.org/map/' + map)

    g.add((prov, has_map, map_image))
