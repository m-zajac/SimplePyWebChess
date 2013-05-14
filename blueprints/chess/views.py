import json
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

        board_data = chessgame.board_manager.serialize(chessgame.board)
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

        data = json.dumps(
            {
                'board': board_data,
                'moves': piece_move_data
            },
            separators=(',', ':')
        )

        return Response(response=data,
                        status=200,
                        mimetype="application/json")
