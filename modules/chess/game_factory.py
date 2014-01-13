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


def make_whites_castling_short():
    """Makes game with whites shot castling possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['Wr1'], (7, 0))

    _game.initPiece(_game.piece_list['BK'], (4, 7))

    return _game


def make_whites_castling_long():
    """Makes game with whites long castling possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['Wr1'], (0, 0))

    _game.initPiece(_game.piece_list['BK'], (4, 7))

    return _game


def make_whites_enpassant():
    """Makes game with whites en passant capture possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['BK'], (4, 7))

    _game.initPiece(_game.piece_list['Wp1'], (5, 4))
    _game.initPiece(_game.piece_list['Bp1'], (4, 6))

    _game.black_moves = True

    return _game


def make_blacks_enpassant():
    """Makes game with whites en passant capture possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['BK'], (4, 7))

    _game.initPiece(_game.piece_list['Wp1'], (5, 1))
    _game.initPiece(_game.piece_list['Bp1'], (4, 3))

    _game.black_moves = False

    return _game


def make_whites_promotion():
    """Makes game with whites promotion possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['BK'], (2, 7))

    _game.initPiece(_game.piece_list['Wp1'], (6, 6))
    _game.initPiece(_game.piece_list['Bp1'], (1, 3))

    _game.black_moves = False

    return _game


def make_blacks_promotion():
    """Makes game with blacks promotion possibility"""
    _board = board.Board()
    _game = game.Game(_board)

    _game.init_new()
    _game.strip()

    _game.initPiece(_game.piece_list['WK'], (4, 0))
    _game.initPiece(_game.piece_list['BK'], (2, 4))

    _game.initPiece(_game.piece_list['Wp1'], (6, 6))
    _game.initPiece(_game.piece_list['Bp1'], (1, 1))

    _game.black_moves = True

    return _game
