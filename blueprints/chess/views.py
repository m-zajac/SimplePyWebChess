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
            move = pieces.PieceMove(data['move'])
            chessgame.move(move)
        else:
            chessgame.move()

        return prepare_game_response(chessgame)

    @blueprint.route('/game/whites_check1', methods=['POST'])
    def whites_check1():
        _game = game_factory.make_whites_check1()
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
        result['move'] = data['move']

    return result


def prepare_game_response(chessgame):
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

    return Response(
        response=json.dumps(
            {
                'game': game_data,
                'moves': piece_move_data,
                'check': chessgame.board_manager.is_check(chessgame.board, chessgame.black_moves),
                'mate': chessgame.board_manager.is_checkmate(chessgame.board, chessgame.black_moves),
                'stalemate': chessgame.board_manager.is_stalemate(chessgame.board, chessgame.black_moves),
            },
            separators=(',', ':')
        ),
        status=200,
        mimetype="application/json"
    )
