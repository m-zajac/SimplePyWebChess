"""Game module"""
import pieces
import board


class Game(object):
    """Game class"""
    def __init__(self, gameboard=None, move_generator=None):
        super(Game, self).__init__()

        self.board_manager = board.BoardManager
        self.board = gameboard
        if not self.board:
            self.board = board.Board()

        self.move_generator = move_generator

        # pieces in game
        self.white_pieces = []
        self.black_pieces = []

        # captures
        self.white_captures = []
        self.black_captures = []

        # game state
        self.black_moves = False
        self.is_check = False
        self.is_checkmate = False

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

            kqpos = [(3, 0), (4, 0)]
            if is_black:
                kqpos = [(4, 0), (3, 0)]

            # queen
            piece_set[kqpos[0]] = pieces.Piece(pieces.TypeQueen, is_black, id_prefix + 'Q')

            # king
            piece_set[kqpos[1]] = pieces.Piece(pieces.TypeKing, is_black, id_prefix + 'K')

            # pawns
            for i in range(8):
                piece_set[(i, 1)] = pieces.Piece(pieces.TypePawn, is_black, id_prefix + 'p' + str(i+1))

            return piece_set

        white_pieces = make_piece_set(False, 'W')
        for pos, piece in white_pieces.iteritems():
            self.board_manager.initPiece(self.board, piece, pos, False)
            self.white_pieces.append(piece)

        black_pieces = make_piece_set(True, 'B')
        for pos, piece in black_pieces.iteritems():
            # symetrical
            pos = (7 - pos[0], 7 - pos[1])
            self.board_manager.initPiece(self.board, piece, pos, False)
            self.black_pieces.append(piece)

        return self

    def strip(self):
        """Strips all pieces off board (for testing purpose)"""
        for row in self.game.squares:
            for square in row:
                piece = square.piece
                if piece:
                    self.capture(piece)

    def move(self, move=None):
        """Validates move and executes it. Returns captured pieces."""
        if not move:
            # empty destination, run move generator
            move = self.move_generator.move(self)

        for move_data in move.moves:
            piece = self.board.squares[move_data[0][0]][move_data[0][1]].piece
            if not piece:
                raise ValueError('Invalid start position')
            if piece.is_black != self.black_moves:
                raise ValueError('Invaid player')

            valid_moves = piece.getMoves(self.board)

            valid_destinations = []
            for valid_move in valid_moves:
                for m in valid_move.moves:
                    valid_destinations.append(m[1])

            if not (move_data[1][0], move_data[1][1]) in valid_destinations:
                raise ValueError('Invalid move destination')

        captures = self.board_manager.move(self.board, move)
        for capture in captures:
            self.capture(capture)

        # check check
        if self.black_moves:
            kingpos = self.board.white_king_pos
        else:
            kingpos = self.board.black_king_pos

        if pieces.TypeKing.checkSafe(kingpos, self.board.squares):
            self.is_check = False
        else:
            self.is_check = True

        # switch player
        self.black_moves = not self.black_moves

        # check checkmate
        available_moves = self.getAllMoves()
        if len(available_moves) == 0:
            self.is_checkmate = True
        else:
            self.is_checkmate = False

        return captures

    def capture(self, piece):
        if piece.is_black:
            self.white_captures.append(piece)
            self.black_pieces.remove(piece)
        else:
            self.black_captures.append(piece)
            self.white_pieces.remove(piece)

        piece.position = None

    def getAllMoves(self):
        """Returns all available moves for current player"""
        moves = []
        for row in self.board.squares:
            for square in row:
                if square.piece:
                    p = square.piece
                    if p.is_black == self.black_moves:
                        for m in p.getMoves(self.board):
                            moves.append(m)

        return moves

    def serialize(self):
        black_captures_data = []
        white_captures_data = []

        for p in self.black_captures:
            black_captures_data.append(self.board_manager.serializePiece(p))

        for p in self.white_captures:
            white_captures_data.append(self.board_manager.serializePiece(p))

        data = {
            'board':            self.board_manager.serialize(self.board),
            'black_moves':      self.black_moves,
            'black_captures':   black_captures_data,
            'white_captures':   white_captures_data,
            'is_check':         self.is_check,
            'is_checkmate':     self.is_checkmate
        }

        return data

    def deserialize(self, game_data):
        self.board_manager.deserialize(self.board, game_data['board']),

        self.black_moves = game_data['black_moves']
        self.is_check = game_data['is_check']
        self.is_checkmate = game_data['is_checkmate']

        self.black_captures = []
        for p in game_data['black_captures']:
            self.black_captures.append(self.board_manager.deserializePiece(p))

        self.white_captures = []
        for p in game_data['white_captures']:
            self.white_captures.append(self.board_manager.deserializePiece(p))

        self.white_pieces = []
        self.black_pieces = []

        for row in self.board.squares:
            for square in row:
                piece = square.piece
                if not piece:
                    continue

                if piece.is_black:
                    self.black_pieces.append(piece)
                else:
                    self.white_pieces.append(piece)
