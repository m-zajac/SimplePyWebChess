from flask import render_template, Response
from modules.chess import game


def init(blueprint):
    # index

    @blueprint.route('')
    def index():
        return render_template('chess/index.html')

    @blueprint.route('/game/init')
    def init():
        chessgame = game.Game()
        chessgame.init_new()

        return Response(response=chessgame.board.serialize(),
                        status=200,
                        mimetype="application/json")
