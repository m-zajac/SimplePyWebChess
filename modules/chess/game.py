"""Game module"""
import pieces
import board


class Game(object):
    """Game class"""
    def __init__(self, gameboard=None, move_generator=None):
        super(Game, self).__init__()

        self.black_moves = False
        self.white_captures = []
        self.black_captures = []

        self.board = gameboard
        if not self.board:
            self.board = board.Board()

        self.move_generator = move_generator

    def init_new(self):
        """Initialize game. self.board must be present."""

        def make_piece_set(is_black, id_prefix):
            piece_set = {}

            # rooks
            piece_set[(0, 0)] = pieces.Piece(pieces.TypeRook, is_black, id_prefix + 'r1')
            piece_set[(7, 0)] = pieces.Piece(pieces.TypeRook, is_black, id_prefix + 'r2')

            # knights
            piece_set[(1, 0)] = pieces.Piece(pieces.TypeKnight, is_black, id_prefix + 'k1')
            piece_set[(6, 0)] = pieces.Piece(pieces.TypeKnight, is_black, id_prefix + 'k2')

            # bishops
            piece_set[(2, 0)] = pieces.Piece(pieces.TypeBishop, is_black, id_prefix + 'b1')
            piece_set[(5, 0)] = pieces.Piece(pieces.TypeBishop, is_black, id_prefix + 'b2')

            # queen
            piece_set[(3, 0)] = pieces.Piece(pieces.TypeQueen, is_black, id_prefix + 'Q')

            # king
            piece_set[(4, 0)] = pieces.Piece(pieces.TypeKing, is_black, id_prefix + 'K')

            # pawns
            for i in range(8):
                piece_set[(i, 1)] = pieces.Piece(pieces.TypePawn, is_black, id_prefix + 'p' + str(i+1))

            return piece_set

        white_pieces = make_piece_set(False, 'W')
        for pos, piece in white_pieces.iteritems():
            self.board.initPiece(piece, pos, False)

        black_pieces = make_piece_set(True, 'B')
        for pos, piece in black_pieces.iteritems():
            # symetrical
            pos = (7 - pos[0], 7 - pos[1])
            self.board.initPiece(piece, pos, False)

        return self

    def move(self, pos_from=None, pos_to=None):
        if not pos_to:
            # empty destination, run move generator
            pos_from, pos_to = self.move_generator.move(self.board, pos_from)

        piece = self.board.squares[pos_from[0]][pos_from[1]].piece
        if not piece:
            raise ValueError('Invalid start position')
        if piece.is_black != self.black_moves:
            raise ValueError('Invaid player')

        valid_destinations = piece.getMoves(pos_from, self.board.squares)
        if not pos_to in valid_destinations:
            raise ValueError('Invalid move destination')

        capture = self.board.movePiece(piece, pos_to)
        if capture:
            if self.black_moves:
                self.black_captures.append(capture)
            else:
                self.white_captures.append(capture)

        self.black_moves = not self.black_moves

        return self
