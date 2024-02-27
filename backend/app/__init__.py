from flask import Flask, make_response, jsonify
from .auth import authenticate
app = Flask(__name__)


@app.route('/')
def index():
    return "Please access the backend using the app."


def create_app():
    from .order import order
    app.register_blueprint(order)
    return app
