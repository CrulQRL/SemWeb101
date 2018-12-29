from convert import g
import rdflib


def get_province_statistics(province):
    hasil = ''
    prov = rdflib.URIRef("http://srabeb.org/provinsi/%s" % province)
    qres = g.query(
        """select ?provinsi ?curah ?hutan ?kelembaban ?kecepatan_angin ?distribusi_penduduk ?jumlah_hari_hujan ?luas_sawah ?presentase_miskin_kota ?presentase_miskin_desa ?penyinaran
        where {
            ?provinsi <http://srabeb.org/type/curah_hujan> ?curah .
            ?provinsi <http://srabeb.org/type/luas_hutan> ?hutan .
            ?provinsi <http://srabeb.org/type/kelembaban> ?kelembaban .
            ?provinsi <http://srabeb.org/type/kecepatan_angin> ?kecepatan_angin .
            ?provinsi <http://srabeb.org/type/distribusi_penduduk> ?distribusi_penduduk .
            ?provinsi <http://srabeb.org/type/jumlah_hari_hujan> ?jumlah_hari_hujan .
            ?provinsi <http://srabeb.org/type/luas_lahan_sawah> ?luas_sawah .
            ?provinsi <http://srabeb.org/type/persentase_penduduk_miskin_(perkotaan)> ?presentase_miskin_kota .
            ?provinsi <http://srabeb.org/type/persentase_penduduk_miskin_perdesaan> ?presentase_miskin_desa .
            ?provinsi <http://srabeb.org/type/rata_rata_penyinaran_matahari> ?penyinaran .
        }
        """, initBindings={'provinsi': prov})

    for row in qres:
        hasil = "provinsi:%s, curah:%s, hutan:%s, kelembaban:%s, kecepatan_angin:%s, distribusi_penduduk:%s, jumlah_hari_hujan:%s, luas_lahan_sawah:%s, persentase_miskin_kota:%s, persentase_miskin_kota:%s, penyinaran:%s" % row
    return hasil
