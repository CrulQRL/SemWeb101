from flask import Flask, render_template, request
import convert
from graph_query import get_province_statistics
from wikidata_query import (
    get_capital_of,
    get_list_of_provinces,
    get_map)

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/provinces')
def provinces():
    results = get_list_of_provinces()

    # print(str(results))
    # for result in results["results"]["bindings"]:
    #     print(result)

    return render_template('provinces_list.html', data=results["results"])


@app.route('/provinces/', methods=['GET'])
def show_province_detail():
    province = request.args.get('p').replace(' ', '_')
    stats = get_province_statistics(province).split(',')
    capital = get_capital_of(province)
    province_map = get_map(province)

    try:
        stats[1].split(':')[1]
    except:
        return "Provinsi '" + province + "' tidak ditemukan"
    return render_template(
        'province.html',
        province=province,
        data=stats,
        capital=capital,
        province_map=province_map
    )


if __name__ == '__main__':
    app.run(debug = True)
