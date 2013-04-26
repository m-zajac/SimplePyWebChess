"""Board module"""


class Square(object):
    """Square on board"""
    def __init__(self, Piece=None):
        super(Square, self).__init__()
        if Piece:
            self.piece = Piece
        else:
            self.piece = None


class Board(object):
    """Board class"""
    def __init__(self):
        self.squares = tuple([
            tuple([
                Square() for x in range(8)
            ]) for i in range(8)
        ])

    def setPiece(self, piece, pos, validate=True):
        pass

    def validatePos(self, pos):
        if not isinstance(pos, tuple):
            raise TypeError(str(type(pos)) + ' is not a tuple!')

        if len(pos) != 2:
            raise ValueError('Invalid position tuple')

        if not self.onBoard(pos):
            raise ValueError('Position out of board!')

    def onBoard(self, position):
        def rangeok(val):
            if val < 0 or val > 7:
                return False
            return True

        if not rangeok(position[0]) or not rangeok(position[1]):
            return False

        return True
