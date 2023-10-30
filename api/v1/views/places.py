#!/usr/bin/python3
"""Contains the places view for the API.
"""

from api.v1.views.__init__ import app_views
from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, abort, request
from models import storage

@app_views.route('/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Get a list of places for a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = city.places
    place_list = [place.to_dict() for place in places]
    return jsonify(place_list)

@app_views.route('/places/<string:place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Get a specific place by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a specific place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})

@app_views.route('/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a new place for a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")

    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    place_name = data["name"]
    new_place = Place(name=place_name, user_id=user_id, city_id=city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a specific place by place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ('id', 'user_id', 'city_id', 'created_at', 'updated_at'):
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict())
