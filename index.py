from flask import Flask, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

from convert import get_data_of, get_capital_of

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/cities')
def cities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""SELECT ?item ?itemLabel WHERE {
    ?item wdt:P31 wd:Q5098.
    SERVICE wikibase:label {bd:serviceParam wikibase:language "id" .}
    }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    # print(str(results))
    # for result in results["results"]["bindings"]:
    #     print(result)

    return render_template('cities.html', data = results["results"])

@app.route('/cities/<province>')
def show_province_detail(province):
    data = get_data_of(province)[0]
    hasil = data.split(',')
    capital = get_capital_of(province)
    return render_template(
        'province.html',
        province = province,
        curah = hasil[1].split(':')[1],
        luas_hutan = hasil[2].split(':')[1],
        kelembaban = hasil[3].split(':')[1],
        kecepatan_angin = hasil[4].split(':')[1],
        capital = capital
    )


if __name__ == '__main__':
   app.run(debug = True)