from flask import Flask, jsonify, request, json
from flask_cors import CORS
from bson import json_util
from start_crawler import start_reactor

import managedb

app = Flask(__name__)
cors = CORS(app, headers=['Content-Type'])
database = managedb.get_db()

@app.route('/')
def get_root():
    resutl = database['index_store'].find_one()
    return "App is working " + resutl['name']


@app.route('/api/urls', methods=['GET'])
def get_urls_list():

    return ["Names"]


if __name__ == '__main__':
    app.run()
