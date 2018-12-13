from flask import Flask, render_template
import convert
from graph_query import get_data_of
from wikidata_query import (
    get_capital_of,
    get_list_of_provinces,
    get_map)

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/provinces')
def provinces():
    results = get_list_of_provinces()

    # print(str(results))
    # for result in results["results"]["bindings"]:
    #     print(result)

    return render_template('provinces_list.html', data=results["results"])


@app.route('/provinces/<province>')
def show_province_detail(province):
    data = get_data_of(province).split(',')
    capital = get_capital_of(province)
    province_map = get_map(province)
    return render_template(
        'province.html',
        province=province,
        data=data,
        capital=capital,
        province_map=province_map
    )


if __name__ == '__main__':
    app.run(debug = True)
