"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Actor
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    user = User.query.filter_by(email = email).first()
    
    if email != user.email or password != user.password :
        return jsonify({"msg": "Bad email or password"}), 401
    print(user)
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@api.route('/actors', methods=['GET'])
def get_all_actors():

    all_actors = Actor.query.all()
    print(all_actors)

    results = list(map(lambda actor : actor.serialize(),all_actors))
    print(results)


    # response_body = {
    #     "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    # }

    return jsonify(results), 200


@api.route('/actors/<int:actors_id>', methods=['GET'])
def get_actor(actors_id):

    single_actor = Actor.query.get(actors_id)
    print("senza serialize", single_actor)
    print("con serialize", single_actor.serialize())

    return jsonify(single_actor.serialize()), 200


@api.route('/actors', methods=['POST'])
def add_actor():

    nombre = request.json.get("nombre", None)                                   # Estraggo i dati dalla richiesta JSON
    nacionalidad = request.json.get("nacionalidad", None)
    print(nombre, nacionalidad)

    if not nombre or not nacionalidad:                                       # Controllo che tutti i campi obbligatori siano presenti
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    new_actor = Actor(nombre = nombre, nacionalidad = nacionalidad)       # Creo un nuovo attore con i dati ricevuti
    db.session.add(new_actor)
    db.session.commit()

    return jsonify({"message" : "actor successfully added"}), 201            # 201 per created