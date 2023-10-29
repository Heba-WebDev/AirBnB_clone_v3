ontains the cities view for the API.
"""

from flask import Blueprint, jsonify, request, abort
from models import storage
from models.state import State
from models.city import City

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
cls = City

@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = state.cities
    city_list = [city.to_dict() for city in cities]
    return jsonify(city_list)

@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = storage.get(cls, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = storage.get(cls, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})

@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")

    city_name = data["name"]
    new_city = cls(name=city_name, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(cls, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
