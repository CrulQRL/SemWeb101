from flask import Flask, render_template, request, jsonify
import convert
from graph_query import (
    get_province_statistics,
    insert_province_description,
    get_province_description,
    get_province_area_and_island_info)
from wikidata_query import (
    get_capital_of,
    get_list_of_provinces,
    get_map,
    get_provinces_capital_data,
    get_data_capital_of_indonesia)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/provinces-list')
def provinces():
    results = get_list_of_provinces()

    return render_template('provinces_list.html', data=results["results"])


@app.route('/province/', methods=['GET'])
def show_province_detail():
    province = request.args.get('p').replace(' ', '_')
    stats = get_province_statistics(province).split(',')
    capital = get_capital_of(province)
    description = get_province_description(province)
    province_map = get_map(province)
    area_info = get_province_area_and_island_info(province).split(',')

    try:
        stats[1].split(':')[1]
    except:
        return "Provinsi '" + province + "' tidak ditemukan"
    return render_template(
        'province.html',
        province=province,
        description=description,
        data=stats,
        capital=capital,
        province_map=province_map,
        area_info=area_info
    )


@app.route('/province/<province>/capital/<capital>')
def capital_of_province(province, capital):
    if capital == 'Jakarta':
        data = get_data_capital_of_indonesia()
    else:
        data = get_provinces_capital_data(province)
    return render_template(
        'capital.html',
        province=province,
        capital=capital,
        data=data
    )


@app.route('/submit-description/', methods=['POST'])
def submit_description():
    desc = request.form['deskripsiInput']
    prov = request.form['provinsi'].replace(' ', '_')

    try:
       insert_province_description(prov, desc)
       return jsonify({
           'status' : 'success',
           'province' : prov,
           'description' : desc
       })
    except:
        return jsonify({
           'status' : 'fail',
           'province' : prov,
           'description' : desc
       })

if __name__ == '__main__':
    app.run(debug = True)
