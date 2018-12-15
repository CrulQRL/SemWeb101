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
