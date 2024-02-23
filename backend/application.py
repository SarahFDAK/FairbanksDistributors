from flask import Flask, make_response, jsonify, request
import json

from app import authenticate
from app import stores
from app import items
from app import order


fd_app = Flask(__name__)


@fd_app.route('/')
def index():
    return "Please access the backend using the app."


@fd_app.route('/login')
@authenticate
def login():
    return make_response(jsonify({"Success": "Authentication code is valid"}), 200)


@fd_app.route('/stores', methods=['GET'])
@authenticate
def get_stores():
    return stores.load()


@fd_app.route('/chips/items', methods=['GET'])
@authenticate
def get_chips():
    return items.load_chips()


@fd_app.route('/freezer_bread/items', methods=['GET'])
@authenticate
def get_freezer_bread():
    return items.load_freezer_bread()


@fd_app.route('/fresh_bread/items', methods=['GET'])
@authenticate
def get_fresh_bread():
    return items.load_fresh_bread()


@fd_app.route('/place_order', methods=['POST', 'GET'])
@authenticate
def place_order():
    order_data = json.loads(request.form['order'])

    resp = order.place(order_data)

    return jsonify(resp)


@fd_app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


if __name__ == "__main__":
    fd_app.run(debug=True)
