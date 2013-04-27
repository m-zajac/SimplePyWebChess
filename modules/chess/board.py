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


class Board(object):
    """Board class"""
    def __init__(self):
        self.squares = tuple([
            tuple([
                Square(not ((i + j) % 2)) for i in range(8)
            ]) for j in range(8)
        ])

        self.white_pieces = {}
        self.black_pieces = {}

    def getDictForPiece(self, piece):
        return self.black_pieces if piece.is_black else self.white_pieces

    def initPiece(self, piece, pos, validate=True):
        """Sets piece on board"""
        if validate and not self.onBoard(pos):
            raise ValueError('Position out of board!')

        piece_dict = self.getDictForPiece(piece)
        piece_dict[piece.id] = {
            'piece': piece,
            'pos':   pos
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
                self.removePiece(captured_piece)
            else:
                # same color, invalid move!
                raise ValueError('Square already occupied!')

        # move
        old_pos = piece_dict[piece.id]['pos']
        self.squares[old_pos[0]][old_pos[1]].piece = None
        self.squares[new_position[0]][new_position[1]].piece = piece
        piece_dict[piece.id]['pos'] = new_position

        return captured_piece

    def removePiece(self, piece):
        """Removes piece from board"""
        piece_dict = self.getDictForPiece(piece)
        pos = piece_dict[piece.id]['pos']
        self.squares[pos[0]][pos[1]].piece = None
        del piece_dict[piece.id]

        return self

    def onBoard(self, position):
        def rangeok(val):
            if val < 0 or val > 7:
                return False
            return True

        if not rangeok(position[0]) or not rangeok(position[1]):
            return False

        return True
