import json
from flask import render_template, Response, request, abort
from modules.chess import game, pieces
from modules.chess.move_generators.gen_random import MoveGenerator as RandomMoveGenerator


def init(blueprint):

    @blueprint.route('')
    def index():
        return render_template('chess/index.html')

    @blueprint.route('/game/init')
    def init():
        chessgame = game.Game()
        chessgame.init_new()

        return Response(response=prepare_response(chessgame),
                        status=200,
                        mimetype="application/json")

    @blueprint.route('/game/move', methods=['POST'])
    def move():
        data = json.loads(request.form.items()[0][0])
        if not 'game_data' in data or not 'move' in data:
            abort(400)

        chessgame = game.Game(None, RandomMoveGenerator())
        chessgame.deserialize(data['game_data']['game'])

        move = pieces.PieceMove(data['move'])
        chessgame.move(move)

        chessgame.move()

        return Response(response=prepare_response(chessgame),
                        status=200,
                        mimetype="application/json")


def prepare_response(chessgame):
    game_data = chessgame.serialize()
    piece_moves = chessgame.getAllMoves()
    piece_move_data = []
    for piece_move in piece_moves:
        start_pos = piece_move.moves[0][0]
        end_pos = piece_move.moves[0][1]
        piece_id = chessgame.board.squares[start_pos[0]][start_pos[1]].piece.id

        piece_move_data.append({
            'pid': piece_id,
            'to':  end_pos
        })

    return json.dumps(
        {
            'game': game_data,
            'moves': piece_move_data
        },
        separators=(',', ':')
    )
