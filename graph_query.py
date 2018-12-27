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

    try:
        g.add((prov, deskripsi, deskripsi_literal))
        return 'berhasil'
    except:
        return 'gagal'
