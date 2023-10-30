#!/usr/bin/python3
"""Contains the places view for the API.
"""

from api.v1.views.__init__ import app_views
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from models import storage

cls = Place

@app_views.route('/api/v1/cities/<string:city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Get a list of places for a specific city"""
    list_places = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        list_places.append(place.to_dict())

    return jsonify(place_list)

@app_views.route('/api/v1/places/<string:place_id>/place_id', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Get a specific place by id"""
    place = storage.get(cls, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/api/v1/places/<string:place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a specific place by place_id"""
    place = storage.get(cls, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/api/v1/cities/<string:city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Create a new place for a specific city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description= "Missing user_id")
    if 'name' not in data:
	abort(400, description="Missing name")

    new_place = cls(**data)
    new_place.city_id = city.id
    new_place.save()

    return jsonify(new_place.to_dict()), 201

@app_views.route('/api/v1/places/<string:place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a specific place by place_id"""
    place = storage.get(cls, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ['id', 'created_at', 'updated_at', 'city_id']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
