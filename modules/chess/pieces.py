"""Pieces module"""
import operator


class Piece(object):
    """Base piece class"""
    def __init__(self, type, position=None):
        super(Piece, self).__init__()

        self.position = position
        self.type = type

    def setPos(self, pos):
        """Sets piece position on board"""
        self.position = pos
        return self

    def getMoves(self, current_pos):
        """Returns available moves offsets"""
        return self.type.getMoves(current_pos)


class TypeKing(object):
    """King"""
    @staticmethod
    def getMoves(current_pos):
        """One square in each direction"""
        moves = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]
        return map(lambda m: tuple(map(operator.add, m, current_pos)), moves)

class TypeQueen(object):
    """Queen"""
    @staticmethod
    def getMoves(current_pos):
        """One+ square in each direction"""
        def rangeok(val):
            if val < 0 or val > 7:
                return False
            return True

        moves = [(x, y) for x in range(-8, 9) for y in range(-8, 9) if (x != 0 or y != 0) and (abs(x) == abs(y) or not all((x,y)))]
        moves = map(lambda m: tuple(map(operator.add, m, current_pos)), moves)
        moves = filter(lambda m: rangeok(m[0]) and rangeok(m[1]), moves)
        return moves
