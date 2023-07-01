import os
from flask import Flask, request, jsonify, url_for
from models import db, User, People, Planet, Favorite
from utils import generate_sitemap, APIException
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

@app.route('/people', methods='POST')
def post_people():
    body = request.json

    if 'name' not in body:
        return jsonify({"message": "Error no se ha enviando 'name' en el body"}), 400
    if 'description' not in body:
        return jsonify({"message": "Error no se ha enviando 'description' en el body"}), 400
    try:
        new_people = People(body['name'], body['description'])
        db.session.add(new_people)
        db.session.commit()
        return jsonify(new_people.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500