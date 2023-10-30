#!/usr/bin/python3
"""create a route /places on the object app_views that returns a JSON"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places(city_id):
    list_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(list_places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place_id(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    if 'name' not in response:
        abort(400, description="Missing name")

    new_place = Place(**response)
    new_place.city_id = city.id
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    response = request.get_json()
    if response is None:
        abort(400, description="Not a JSON")

    keys_to_ignore = ['id', 'created_at', 'updated_at', 'city_id']

    for key, value in response.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
