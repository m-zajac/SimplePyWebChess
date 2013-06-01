import board
import game
import pieces


def make_whites_check1():
    """Makes game with whites check situation"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()

    _game.move(pieces.PieceMove(((4, 1), (4, 3))))
    _game.move(pieces.PieceMove(((4, 6), (4, 4))))
    _game.move(pieces.PieceMove(((6, 0), (5, 2))))
    _game.move(pieces.PieceMove(((5, 6), (5, 5))))
    _game.move(pieces.PieceMove(((5, 2), (4, 4))))
    _game.move(pieces.PieceMove(((5, 5), (4, 4))))
    _game.move(pieces.PieceMove(((3, 0), (7, 4))))

    return _game


def make_whites_checkmate1():
    """Makes game with whites check situation"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()

    _game.move(pieces.PieceMove(((4, 1), (4, 2))))
    _game.move(pieces.PieceMove(((5, 6), (5, 5))))
    _game.move(pieces.PieceMove(((3, 1), (3, 2))))
    _game.move(pieces.PieceMove(((6, 6), (6, 4))))
    _game.move(pieces.PieceMove(((3, 0), (7, 4))))

    return _game
