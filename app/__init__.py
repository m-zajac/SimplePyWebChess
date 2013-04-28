from flask import Flask
from views import init
from blueprints.chess import chess


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug

    app.register_blueprint(chess, url_prefix='/chess')

    init(app)

    return app
