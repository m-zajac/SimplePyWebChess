"""Board module"""
import pieces
import json


class Square(object):
    """Square on board"""
    def __init__(self, is_black, Piece=None):
        super(Square, self).__init__()
        if Piece:
            self.piece = Piece
        else:
            self.piece = None

        self.is_black = is_black


class Board(object):
    """Board class"""

    # piece types dictionary
    types_dict = {
        'K': pieces.TypeKing,
        'Q': pieces.TypeQueen,
        'b': pieces.TypeBishop,
        'k': pieces.TypeKnight,
        'r': pieces.TypeRook,
        'p': pieces.TypePawn
    }

    def __init__(self):
        self.squares = [[Square(not ((i + j) % 2)) for i in range(8)] for j in range(8)]
        self.squares_reversed = [[self.squares[7-i][7-j] for i in range(8)] for j in range(8)]

        self.white_pieces = {}
        self.white_captures = []
        self.black_pieces = {}
        self.black_captures = []

    def getDictForPiece(self, piece):
        return self.black_pieces if piece.is_black else self.white_pieces

    def initPiece(self, piece, pos, validate=True):
        """Sets piece on board"""
        if validate and not self.onBoard(pos):
            raise ValueError('Position out of board!')

        piece_dict = self.getDictForPiece(piece)
        piece_dict[piece.id] = {
            'piece': piece,
            'pos':   pos,
            'moves': 0
        }
        self.squares[pos[0]][pos[1]].piece = piece

        return self

    def movePiece(self, piece, new_position, validate=True):
        """Moves piece. If there is capture, captured piece is returned. Otherwise None is returned"""
        if validate and not self.onBoard(new_position):
            raise ValueError('Position out of board!')

        piece_dict = self.getDictForPiece(piece)
        if not piece.id in piece_dict:
            raise ValueError('There is no piece ' + piece.id + ' on board')

        # capture
        captured_piece = self.squares[new_position[0]][new_position[1]].piece
        if captured_piece:
            if captured_piece.is_black != piece.is_black:
                # take captured piece off board
                self.removePiece(captured_piece, True)
            else:
                # same color, invalid move!
                raise ValueError('Square already occupied!')

        # move
        old_pos = piece_dict[piece.id]['pos']
        self.squares[old_pos[0]][old_pos[1]].piece = None
        self.squares[new_position[0]][new_position[1]].piece = piece
        piece_dict[piece.id]['pos'] = new_position
        piece_dict[piece.id]['moves'] += 1
        piece.moves_count += 1

        return captured_piece

    def removePiece(self, piece, capture=False):
        """Removes piece from board"""
        piece_dict = self.getDictForPiece(piece)
        pos = piece_dict[piece.id]['pos']
        self.squares[pos[0]][pos[1]].piece = None
        del piece_dict[piece.id]

        if capture:
            if piece.is_black:
                self.white_captures.append(piece)
            else:
                self.black_captures.append(piece)

        return self

    def onBoard(self, position):
        def rangeok(val):
            if val < 0 or val > 7:
                return False
            return True

        if not rangeok(position[0]) or not rangeok(position[1]):
            return False

        return True

    def serialize(self):
        reverse_types_dict = {v: k for k, v in self.types_dict.items()}

        def serialize_set(set):
            result = {}
            for id, setdata in set.iteritems():
                result[id] = {
                    't':  reverse_types_dict[setdata['piece'].type],
                    'p':   setdata['pos'],
                    'm': setdata['moves']
                }

            return result

        whites = serialize_set(self.white_pieces)
        blacks = serialize_set(self.black_pieces)

        result = {
            'whites': whites,
            'blacks': blacks
        }

        return json.dumps(result, separators=(',', ':'))

    def deserialize(self, data):
        data = json.loads(data)

        self.__init__()

        def restore_set(data, destination_set, is_black):
            for id, setdata in data.iteritems():
                ptype = self.types_dict[setdata['t']]
                p = pieces.Piece(ptype, is_black, id)
                self.initPiece(p, tuple(setdata['p']))
                destination_set[id]['moves'] = setdata['m']

        restore_set(data['whites'], self.white_pieces, False)
        restore_set(data['blacks'], self.black_pieces, True)

        return self
