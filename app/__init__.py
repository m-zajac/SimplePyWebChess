from flask import Flask
from views import init
from blueprints.chess import chess


def create_app():
    app = Flask(__name__)
    init(app)

    app.register_blueprint(chess, url_prefix='/chess')

    return app
