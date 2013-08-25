import json
from flask import render_template, Response, request, abort
from modules.chess import game, pieces
from modules.chess.move_generators.gen_random import MoveGenerator as RandomMoveGenerator
import modules.chess.game_factory as game_factory


def init(blueprint):

    @blueprint.route('')
    def index():
        return render_template('chess/index.html')

    @blueprint.route('/game/init', methods=['POST'])
    def init():
        chessgame = game.Game(None, RandomMoveGenerator())
        chessgame.init_new()

        return prepare_game_response(chessgame)

    @blueprint.route('/game/move', methods=['POST'])
    def move():
        data = parse_game_request()

        chessgame = data['game']

        # move
        if 'move' in data:
            move = data['move']
            chessgame.move(move)
        else:
            chessgame.move()

        return prepare_game_response(chessgame)

    # Game tests
    @blueprint.route('/game/whites_check1', methods=['POST'])
    def whites_check1():
        _game = game_factory.make_whites_check1()
        return prepare_game_response(_game)

    @blueprint.route('/game/whites_checkmate1', methods=['POST'])
    def whites_checkmate1():
        _game = game_factory.make_whites_checkmate1()
        return prepare_game_response(_game)

    @blueprint.route('/game/whites_castling_short', methods=['POST'])
    def whites_castling_short():
        _game = game_factory.make_whites_castling_short()
        return prepare_game_response(_game)

    @blueprint.route('/game/whites_castling_long', methods=['POST'])
    def whites_castling_long():
        _game = game_factory.make_whites_castling_long()
        return prepare_game_response(_game)


def parse_game_request(chessgame=None):
    try:
        data = json.loads(request.form.items()[0][0])
    except IndexError:
        data = None

    if not chessgame:
        chessgame = game.Game(None, RandomMoveGenerator())
        chessgame.init_new()

    if data and 'game_data' in data:
        chessgame.deserialize(data['game_data']['game'])

    result = {
        'game': chessgame,
    }

    if data and 'move' in data:
        result['move'] = chessgame.deserialize_move(data['move'])

    return result


def prepare_game_response(chessgame):
    game_data = chessgame.serialize()
    piece_moves = chessgame.getAllMoves()
    piece_move_data = []
    for piece_move in piece_moves:
        start_pos = piece_move.moves[0][0]
        piece_id = chessgame.board.squares[start_pos[0]][start_pos[1]].piece.id

        piece_move_data.append({
            'pid': piece_id,
            'move': chessgame.serialize_move(piece_move)
        })

    return Response(
        response=json.dumps(
            {
                'game': game_data,
                'moves': piece_move_data
            },
            separators=(',', ':')
        ),
        status=200,
        mimetype="application/json"
    )
