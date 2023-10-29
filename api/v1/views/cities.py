#!/usr/bin/python3
'''Contains the cities view for the API.'''
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def get_create_update_delete_cities(state_id=None, city_id=None):
    '''Get, create, update, or delete cities.'''
    state = storage.get(State, state_id)

    if request.method == 'GET':
        if state is None:
            abort(404)
        if city_id is None:
            return jsonify([city.to_dict() for city in state.cities])
        else:
            city = storage.get(City, city_id)
            if city is None or city.state_id != state.id:
                abort(404)
            return jsonify(city.to_dict())

    if request.method == 'POST':
        if state is None:
            abort(404)
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        data['state_id'] = state.id
        city = City(**data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201

    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if city is None or city.state_id != state.id:
            abort(404)
        data = request.get_json(silent=True)
        if data is None:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ('id', 'state_id', 'created_at', 'updated_at'):
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())

    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if city is None or city.state_id != state.id:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
