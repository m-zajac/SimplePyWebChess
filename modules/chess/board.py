"""Board module"""
import pieces


class Square(object):
    """Square on board"""
    def __init__(self, is_black, Piece=None):
        super(Square, self).__init__()
        if Piece:
            self.piece = Piece
        else:
            self.piece = None

        self.is_black = is_black

    def __eq__(self, other):
        return self.piece == other.piece and self.is_black == other.is_black


class Board(object):
    """Board class
    This object will probably be frequently copied, so it's just data. Methods for managing board are in BoardManager class
    """
    def __init__(self):
        """Initialize board"""
        self.squares = [[Square(not ((i + j) % 2)) for i in range(8)] for j in range(8)]

        # symmetrical board, for moving black pieces
        self.squares_reversed = [[self.squares[7-j][7-i] for i in range(8)] for j in range(8)]

        # kings positions
        self.white_king_pos = None
        self.black_king_pos = None


class BoardManager(object):
    """Board manager class"""

    # piece types dictionary
    types_dict = {
        'K': pieces.TypeKing,
        'Q': pieces.TypeQueen,
        'b': pieces.TypeBishop,
        'k': pieces.TypeKnight,
        'r': pieces.TypeRook,
        'p': pieces.TypePawn
    }

    @staticmethod
    def getDictForPiece(board, piece):
        return board.black_pieces if piece.is_black else board.white_pieces

    @staticmethod
    def initPiece(board, piece, pos, validate=True):
        """Sets piece on board"""
        if validate and not BoardManager.onBoard(pos):
            raise ValueError('Position out of board!')

        piece.position = pos

        board.squares[pos[0]][pos[1]].piece = piece

        if piece.type == pieces.TypeKing:
            if piece.is_black:
                board.black_king_pos = pos
            else:
                board.white_king_pos = pos

    @staticmethod
    def move(board, move_object):
        """Moves piece. Returns captured pieces."""
        captured_pieces = []
        for move in move_object.moves:
            start_pos = move[0]
            end_pos = move[1]

            piece = board.squares[start_pos[0]][start_pos[1]].piece
            if not piece:
                raise ValueError('Invalid move position!')

            captured_piece = board.squares[end_pos[0]][end_pos[1]].piece
            if captured_piece:
                if captured_piece.is_black == piece.is_black:
                    # same color, invalid move!
                    raise ValueError('Invalid move, square occupied!')

                captured_piece.position = None
                captured_pieces.append(captured_piece)

            # move
            board.squares[start_pos[0]][start_pos[1]].piece = None
            board.squares[end_pos[0]][end_pos[1]].piece = piece
            piece.position = end_pos
            piece.moves_count += 1

            # transformation
            if move_object.transformation:
                pos, trans_piece_type = move_object.transformation
                trans_piece = board.squares[pos[0]][pos[1]].piece
                if trans_piece:
                    trans_piece.type = trans_piece_type

            if piece.type == pieces.TypeKing:
                if piece.is_black:
                    board.black_king_pos = piece.position
                else:
                    board.white_king_pos = piece.position

        return captured_pieces

    @staticmethod
    def removePiece(board, piece):
        """Removes piece from board"""
        pos = piece.position
        board.squares[pos[0]][pos[1]].piece = None
        piece.position = None

    @staticmethod
    def onBoard(position):
        def rangeok(val):
            if val < 0 or val > 7:
                return False
            return True

        if not rangeok(position[0]) or not rangeok(position[1]):
            return False

        return True

    @staticmethod
    def serializePiece(piece):
        if piece is None:
            return None

        reverse_types_dict = {v: k for k, v in BoardManager.types_dict.items()}

        return {
            'id': piece.id,
            't':  reverse_types_dict[piece.type],
            'p':  piece.position,
            'm':  piece.moves_count,
            'b':  piece.is_black
        }

    @staticmethod
    def deserializePiece(piecedata):
        if not piecedata:
            return None

        ptype = BoardManager.types_dict[piecedata['t']]
        p = pieces.Piece(ptype, piecedata['b'], piecedata['id'])
        p.moves_count = piecedata['m']
        if piecedata['p']:
            p.position = tuple(piecedata['p'])

        return p

    @staticmethod
    def serialize(board):
        pieces = []
        for row in board.squares:
            for square in row:
                p = square.piece
                if p:
                    pieces.append(p)

        result = {}
        for p in pieces:
            result[p.id] = BoardManager.serializePiece(p)

        return result

    @staticmethod
    def deserialize(board, data):
        board.__init__()

        for id, piecedata in data.iteritems():
            p = BoardManager.deserializePiece(piecedata)
            BoardManager.initPiece(board, p, p.position)
