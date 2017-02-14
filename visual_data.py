from flask import Flask
from pymongo import MongoClient
from flask import render_template, jsonify


app = Flask(__name__, static_url_path='/static')

def get_db():
    client = MongoClient('localhost:27017')
    db = client.flask_test
    return db


@app.route('/api/get_data', methods=['GET'])
def get_data():
    data = {}

    for elem in db.world_bank.find():
        """ Structure of data:

                "Arab Republic of Egypt": {
                    "lendprojectscost": 2404430000,
                    "projects_name": [
                        "EG - Helwan South Power Project",
                        "Youth Employment"
                    ]
                },
               """
        try:
            country_dict = data[elem['countryname']]
            country_dict['projects_name'].append(elem['project_name'])
            country_dict['lendprojectscost'] += int(elem['lendprojectcost'])
        except KeyError:
            data[elem['countryname']] = {}
            country_dict = data[elem['countryname']]
            country_dict['projects_name'] = []
            country_dict['projects_name'].append(elem['project_name'])
            country_dict['lendprojectscost'] = int(elem['lendprojectcost'])

    return jsonify(data)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')




if __name__ == '__main__':
    db = get_db()
    app.run()





