"""Pieces module"""
import operator


class Piece(object):
    """Base piece class"""
    def __init__(self, type, is_black, id=None):
        super(Piece, self).__init__()

        self.id = id
        self.type = type
        self.is_black = is_black

    def getMoves(self, current_pos, squares):
        """Returns available moves offsets"""
        return self.type.getMoves(self, current_pos, squares)

    @staticmethod
    def add_move_to_pos(move, pos):
        """Adds absolute move coordinates to given position"""
        return tuple(map(operator.add, move, pos))

    @staticmethod
    def pos_in_squares(pos, squares):
        """Checks if position range is valid"""
        return pos[0] >= 0 and pos[0] < len(squares) and pos[1] >= 0 and pos[1] < len(squares[pos[0]])

    @staticmethod
    def map_abs_moves_to_squares(piece, position, moves, squares):
        """Maps absolute moves to board positions"""
        def filter_obstacles(piece, position, squares):
            square = squares[position[0]][position[1]]
            return square.piece is None or square.piece.is_black != piece.is_black

        positions = map(lambda m: Piece.add_move_to_pos(m, position), moves)
        positions = filter(lambda p: Piece.pos_in_squares(p, squares), positions)
        positions = filter(lambda p: filter_obstacles(piece, p, squares), positions)
        return positions


class TypeKing(object):
    """King"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """One square in each direction"""
        moves = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)


class TypeQueen(object):
    """Queen"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """One+ square in each direction"""
        moves = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if (x != 0 or y != 0) and (abs(x) == abs(y) or not all((x, y)))]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)


class TypeBishop(object):
    """Bishop"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """One+ square in each diagonal direction"""
        moves = [(x, y) for x in range(-7, 8) for y in range(-7, 8) if x != 0 and y != 0 and abs(x) == abs(y)]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)


class TypeKnight(object):
    """Knight"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """L moves"""
        moves = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)


class TypeRook(object):
    """Rook"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """Horizontal + vertical moves"""
        moves = [((x, 0), (-x, 0), (0, x), (0, -x)) for x in range(0, 8)]
        moves = [item for sublist in moves for item in sublist]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)


class TypePawn(object):
    """Pawn"""
    @staticmethod
    def getMoves(piece, current_pos, squares):
        """1 square up"""
        moves = [(0, 1)]
        return Piece.map_abs_moves_to_squares(piece, current_pos, moves, squares)
