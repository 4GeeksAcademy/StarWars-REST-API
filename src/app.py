"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people', methods=['POST'])
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
    
@app.route('/people', methods=['GET'])
def get_all_people():
    all_people = People.query.all()
    
    if all_people is not None:
        return jsonify([people.serialize() for people in all_people]), 200
    else:
        return jsonify({"message": "People not found"}), 404
    
@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    people = People.query.get(id)

    if people is not None:
        return jsonify(people.serialize()), 200
    else:
        return jsonify({"message": "That people hasn't been found"}), 404
    
@app.route('/planet', methods=['POST'])
def post_planet():
    body = request.json

    if 'name' not in body:
        return jsonify({"message": "Error no se ha enviando 'name' en el body"}), 400
    if 'description' not in body:
        return jsonify({"message": "Error no se ha enviando 'description' en el body"}), 400
    try:
        new_planet = Planet(body['name'], body['description'])
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.serialize()), 200

    except Exception as err:
        return jsonify({"message": err}), 500
    

@app.route('/planets', methods=['GET'])
def get_all_planet():
    all_planets = Planet.query.all()
    
    if all_planets is not None:
        return jsonify([planet.serialize() for planet in all_planets]), 200
    else:
        return jsonify({"message": "People not found"}), 404
    

@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    planet = Planet.query.get(id)

    if planet is not None:
        return jsonify(planet.serialize()), 200
    else: 
        return jsonify({"message": "That planet hasn't been found"}), 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
