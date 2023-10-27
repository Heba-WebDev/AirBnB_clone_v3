#!/usr/bin/python3
""" Flask API """
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
""" Creates Flask instant """
app_host = getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exception):
    """ Calls storage.close() """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ Handles 404 Not Found """
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    app_host = getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
