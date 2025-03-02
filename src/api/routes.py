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


@api.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):

    single_actor = Actor.query.get(actor_id)
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


@api.route('/actors/<int:actor_id>', methods=['DELETE'])
def delete_actor(actor_id):

    actor = Actor.query.get(actor_id)         #Cerca l'attore nel database

    if not actor:
        return jsonify({"error": "Actor not found"}), 404             
    
    db.session.delete(actor)
    db.session.commit()

    return jsonify ({"message": f"Actor {actor.nombre} successfully deleted"}), 200


@api.route('/actors/<int:actor_id>', methods=['PUT'])
def modify_actor(actor_id):

    actor = Actor.query.get(actor_id)

    if not actor:
        return jsonify({"error": "Actor not found"}), 404        

    nombre = request.json.get("nombre", None)
    nacionalidad = request.json.get("nacionalidad", None)

    if nombre :                                                # Se i nuovi dati sono forniti, aggiorna i campi dell'attore. actor.nombre rappresente il nome gia presente, mentre nombre il nome della req HTTP
        actor.nombre = nombre
    if nacionalidad :
        actor.nacionalidad = nacionalidad 

    db.session.commit()

    return jsonify ({"message": "Actor successfully modified"}), 200