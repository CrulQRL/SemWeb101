from rdflib import URIRef, BNode, Literal, Graph, Namespace
import pandas
import rdflib


g = Graph()


def extract_luas_hutan():
    data = pandas.read_csv('src/hutan.csv')
    luas = URIRef('http://srabeb.org/type/luas_hutan')

    for _, row in data.iterrows():
        province_name = row['Provinsi']
        province = URIRef('http://srabeb.org/provinsi/' + province_name)

        province_forest_area = row[
            'JumlahLuasDaratandanPerairanKawasanHutan(Ha)'
            ]
        forest_area = Literal(province_forest_area)

        g.add((province, luas, forest_area))


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
            g.add((province, kelembaban, kelembaban_literal))
            g.add((province, kec_angin, kecepatan_literal))
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
            g.add((province, jumlah_curah_hujan, curah_hujan_literal))
        else:
            print('Provinsi tidak ditemukan: ' + province_name)

def extract_info_faktor_ketahanan_pangan():
    #Berdasarkan Proposal Gemastik Bidang Penambangan Data, Tim BukaAjaBukaData
    data = pandas.read_csv('src/ketahanan_pangan.csv')
    columns = data.columns
    baseURIRef = 'http://srabeb.org/type/'

    for _, row in data.iterrows():
        province_name = row['Provinsi']
        province = URIRef('http://srabeb.org/provinsi/' + province_name)
        
        for col in data.columns:
            info_type_name = col.lower().replace("-","_").replace(" ","_")
            info_type_uri = URIRef(baseURIRef + info_type_name)
            info_value = Literal(row[col])
            if province:
                g.add((province, info_type_uri, info_value))
            else:
                print('Provinsi tidak ditemukan: ' + province_name)

extract_luas_hutan()
extract_kelembaban_dan_angin()
extract_curah_hujan()
extract_info_faktor_ketahanan_pangan()

# n = Namespace('http://srabeb.org/provinsi/')
