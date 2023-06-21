from flask import Flask, render_template

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
    return render_template('menu.html', entities=entities)

@app.route('/entity/<entity>')
def entity(entity):
    table_data = [
        {'id': 1, 'name': 'Entity 1'},
        {'id': 2, 'name': 'Entity 2'},
        {'id': 3, 'name': 'Entity 3'},
        {'id': 4, 'name': 'Entity 4'},
        {'id': 5, 'name': 'Entity 5'}
    ]

    return render_template('entity.html', entity=entity, table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)