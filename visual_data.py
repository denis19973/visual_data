from flask import Flask
from pymongo import MongoClient
from flask import render_template, Response
from country_validator import validate_country
import json


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

                "USA": {
                    "lendprojectscost": 2404430000,
                    "projects_name": [
                        "EG - Helwan South Power Project",
                        "Youth Employment"
                    ]
                },
               """

        valid_name = validate_country(elem['countryname'])
        try:

            country_dict = data[valid_name]
            country_dict['projects_name'].append(elem['project_name'])
            country_dict['lendprojectscost'] += int(elem['lendprojectcost'])
        except KeyError:
            data[valid_name] = {}
            country_dict = data[valid_name]
            country_dict['projects_name'] = []
            country_dict['projects_name'].append(elem['project_name'])
            country_dict['lendprojectscost'] = int(elem['lendprojectcost'])


    return Response(json.dumps(data), mimetype='application/json')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')




if __name__ == '__main__':
    db = get_db()
    app.run()





