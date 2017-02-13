from flask import Flask
from pymongo import MongoClient
from flask import jsonify


app = Flask(__name__)

def get_db():
    client = MongoClient('localhost:27017')
    db = client.flask_test
    return db


@app.route('/get_data', methods=['GET'])
def hello_world():
    data = {}

    for elem in db.world_bank.find():
        # Structure of data
        # {'project_name': {'country_name': 'UK', 'lendprojectcost': 1000}}
        data[elem['project_name']] = dict(country_name=elem['countryname'], lendprojectcost=elem['lendprojectcost'])

    return jsonify(data)


if __name__ == '__main__':
    db = get_db()
    app.run()





