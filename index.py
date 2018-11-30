from flask import Flask, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/cities')
def cities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""SELECT ?item ?itemLabel WHERE {
    ?item wdt:P31 wd:Q5098.
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(str(results))
    # for result in results["results"]["bindings"]:
    #     print(result)

    return render_template('hello.html', data = results["results"])

if __name__ == '__main__':
   app.run(debug = True)