from flask import Flask, render_template, request, abort
import Oracle_connection

app = Flask(__name__)

entities = [
    {'name': 'presenter', 'display_name': 'Presenter'},
    {'name': 'product', 'display_name': 'Product'},
    {'name': 'agency', 'display_name': 'Agency'},
    {'name': 'tv_campaign', 'display_name': 'TV Campaign'},
    {'name': 'billboard_campaign', 'display_name': 'Billboard Campaign'},
    {'name': 'internet_campaign', 'display_name': 'Internet Campaign'}
]


@app.route('/')
def menu():
    return render_template('main.html')


# get table from post request, then get table data from oracle connection
@app.route('/table', methods=['GET'])
def table():
    print("request.form")
    # get table name from post request
    table_name = request.args.get('button')
    print(table_name)
    # get table data from oracle connection
    if table_name == 'presenter':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.get_presenters())
    elif table_name == 'product':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.get_products())
    elif table_name == 'campaign':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.get_campaigns())
    else:
        abort(404)

    return render_template('display_table.html', table_data=table_data, table_name=table_name)


@app.route('/query', methods=['GET'])
def query():
    print("request.form")
    # get table name from post request
    query = request.args.get('query')
    print(query)
    # get table data from oracle connection
    table_data = Oracle_connection.convert_to_json(*Oracle_connection.apply_query(query))
    return render_template('display_table.html', table_data=table_data, table_name=query)


@app.route('/prepared', methods=['GET'])
def prepared():
    # get table name from post request
    query = request.args.get('query')
    print(query)
    if query == 'kind':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.get_amount_by_kind())
        return render_template('display_table.html', table_data=table_data, table_name=query)
    elif query == 'excellent':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.get_excelent_products())
        return render_template('display_table.html', table_data=table_data, table_name="our products with excellent "
                                                                                       "ratings")
    elif query == 'campaigns':
        table_data = Oracle_connection.convert_to_json(*Oracle_connection.best_campaigns())
        return render_template('display_table.html', table_data=table_data, table_name="our best campaigns")



if __name__ == '__main__':
    app.run(debug=True)
