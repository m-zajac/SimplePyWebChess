"""Pieces module"""

from collections import OrderedDict
from modules.utils import LazyDict


# piece types dictionary
types_dict = LazyDict()
types_dict.addLazy('K', lambda: TypeKing)
types_dict.addLazy('Q', lambda: TypeQueen)
types_dict.addLazy('b', lambda: TypeBishop)
types_dict.addLazy('k', lambda: TypeKnight)
types_dict.addLazy('r', lambda: TypeRook)
types_dict.addLazy('p', lambda: TypePawn)


class PieceMove(object):
    """Piece move object
    One move can be 1 or 2 piece moves (castling) + one transformation (pawn at the end of the board)
    Move positions are absolute
    """
    def __init__(self, *vargs):
        # move = ((from_x, from_y), (to_x, to_y))
        if vargs:
            self.moves = vargs
        else:
            self.moves = []

        # format: tuple - (position, type)
        # params:
        #   position: Piece position after move
        #   type: TypeQueen, TypeRook ...
        self.transformation = None

        # piece to capture
        self.capture = None

    def rotate(self):
        """Transforms coordinates to other player"""
        self.moves = map(lambda m: ((7 - m[0][0], 7 - m[0][1]), (7 - m[1][0], 7 - m[1][1])), self.moves)
        if self.transformation:
            pos = self.transformation[0]
            pos = (7 - pos[0], 7 - pos[1])
            self.transformation = (pos, self.transformation[1])

    def serialize(self):
        reverse_types_dict = {v: k for k, v in types_dict.items()}

        return {
            'moves': self.moves,
            'tp': self.transformation[0] if self.transformation else None,
            'tt': reverse_types_dict[self.transformation[1]] if self.transformation else None,
            'c': self.capture.serialize() if self.capture else None,
        }

    @staticmethod
    def deserialize(data):
        transformation = None
        if 'tt' in data and data['tt']:
            type = types_dict[data['tt']]
            pos = data['tp']

            transformation = (pos, type)

        capture = None
        if 'c' in data:
            capture = Piece.deserialize(data['c'])

        move = PieceMove(*data['moves'])
        move.transformation = transformation
        move.capture = capture

        return move

    def __str__(self):
        return "moves: {m}, trans: {t}, cap: {c}".format(m=self.moves, t=self.transformation, c=self.capture)


class Piece(object):
    """Base piece class"""
    def __init__(self, type, is_black, id=None):
        super(Piece, self).__init__()

        self.id = id
        self.type = type
        self.is_black = is_black
        self.moves_count = 0
        self.position = None

    def getMoves(self, board):
        """Returns available moves offsets
        Returned moves are absolute
        """
        if self.position is None:
            return []

        if self.is_black:
            moves = self.type.getMoves(self, (7 - self.position[0], 7 - self.position[1]), board.squares_reversed)
            map(lambda m: m.rotate(), moves)
        else:
            moves = self.type.getMoves(self, self.position, board.squares)

        # filter by kings safety
        moves = filter(lambda m: TypeKing.checkSafeAfterMove(m, board), moves)
        return moves

    def serialize(self):
        reverse_types_dict = {v: k for k, v in types_dict.items()}

        return {
            'id': self.id,
            't': reverse_types_dict[self.type],
            'p': self.position,
            'm': self.moves_count,
            'b': self.is_black
        }

    @staticmethod
    def deserialize(data):
        if not data:
            return None

        ptype = types_dict[data['t']]
        p = Piece(ptype, data['b'], data['id'])
        p.moves_count = data['m']
        if data['p']:
            p.position = tuple(data['p'])

        return p

    def __eq__(self, other):
        return self.id == other.id and self.type == other.type and self.is_black == other.is_black

    def __str__(self):
        name = 'Black' if self.is_black else 'White'
        name += ' ' + str(self.id) + ' (' + str(self.moves_count) + ' moves)'
        return name

    def __repr__(self):
        return self.__str__()


class TypeBishop(object):
    """Bishop"""

    value = 3

    @staticmethod
    def getMoves(piece, position, squares):
        """One+ square in each diagonal direction"""
        position_list = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                for d in range(1, 8):
                    x, y = position[0] + i * d, position[1] + j * d

                    if max(x, y) > 7 or min(x, y) < 0:
                        break

                    o = squares[x][y].piece
                    if o:
                        if o.is_black == piece.is_black:
                            break
                        else:
                            position_list.append((x, y))
                            break

                    position_list.append((x, y))

        return [PieceMove((position, p)) for p in position_list]


class TypeRook(object):
    """Rook"""

    value = 5

    @staticmethod
    def getMoves(piece, position, squares):
        """Horizontal + vertical moves"""
        position_list = []
        for i in range(4):
            for d in range(1, 8):
                if i == 0:
                    x, y = position[0] + d, position[1]
                elif i == 1:
                    x, y = position[0] - d, position[1]
                elif i == 2:
                    x, y = position[0], position[1] + d
                else:
                    x, y = position[0], position[1] - d

                if max(x, y) > 7 or min(x, y) < 0:
                    break

                o = squares[x][y].piece
                if o:
                    if o.is_black == piece.is_black:
                        break
                    else:
                        position_list.append((x, y))
                        break

                position_list.append((x, y))

        return [PieceMove((position, p)) for p in position_list]


class TypeQueen(object):
    """Queen"""

    value = 9

    @staticmethod
    def getMoves(piece, position, squares):
        return TypeRook.getMoves(piece, position, squares) + TypeBishop.getMoves(piece, position, squares)


class TypeKnight(object):
    """Knight"""

    value = 3

    @staticmethod
    def getMoves(piece, position, squares):
        """L moves"""
        position_list = []
        offsets = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for offset in offsets:
            x, y = position[0] + offset[0], position[1] + offset[1]

            if max(x, y) > 7 or min(x, y) < 0:
                continue

            o = squares[x][y].piece
            if o:
                if o.is_black == piece.is_black:
                    continue
                else:
                    position_list.append((x, y))
                    continue

            position_list.append((x, y))

        return [PieceMove((position, p)) for p in position_list]


class TypePawn(object):
    """Pawn"""

    value = 1

    @staticmethod
    def getMoves(piece, position, squares):
        moves = []
        offsets = [(0, 1)]
        # if first move - may be 2 squares
        if piece.moves_count == 0 and position[1] == 1:
            offsets.append((0, 2))

        for offset in offsets:
            x, y = position[0] + offset[0], position[1] + offset[1]

            if max(x, y) > 7 or min(x, y) < 0:
                continue

            # if first offset is blocked - stop
            if squares[x][y].piece:
                break

            if position[1] == 6:
                # promotion
                types = (TypeQueen, TypeKnight)
                for t in types:
                    move = PieceMove((position, (x, y)))
                    move.transformation = ((x, y), t)
                    moves.append(move)
            else:
                moves.append(PieceMove((position, (x, y))))

        # check attacks
        attacks = [(1, 1), (-1, 1)]
        for attack in attacks:
            x, y = position[0] + attack[0], position[1] + attack[1]

            if max(x, y) > 7 or min(x, y) < 0:
                continue

            o = squares[x][y].piece
            if not o or o.is_black == piece.is_black:
                continue

            if position[1] == 6:
                # promotion
                types = (TypeQueen, TypeKnight)
                for t in types:
                    move = PieceMove((position, (x, y)))
                    move.transformation = ((x, y), t)
                    moves.append(move)
            else:
                moves.append(PieceMove((position, (x, y))))

        # en passant
        if position[1] == 4:
            opponent_positions = [(1, 0), (-1, 0)]
            for op in opponent_positions:
                x, y = position[0] + op[0], position[1] + op[1]

                if max(x, y) > 7 or min(x, y) < 0:
                    continue

                o = squares[x][y].piece
                if not o or o.is_black == piece.is_black:
                    continue
                if o.type != TypePawn or o.moves_count != 1:
                    continue

                move = PieceMove((position, (x, y + 1)))
                move.capture = o
                moves.append(move)

        # promotion
        # if position[1] == 6:
        #     x, y = position[0], position[1] + 1

        #     if max(x, y) <= 7 and min(x, y) >= 0:
        #         o = squares[x][y].piece
        #         if not o:
        #             # promotion available
        #             types = (TypeQueen, TypeKnight)
        #             for t in types:
        #                 move = PieceMove((position, (x, y)))
        #                 move.transformation = ((x, y), t)
        #                 moves.append(move)

        return moves


class TypeKing(object):
    """King"""

    value = 1000
    threats_diagonal = set([TypeQueen, TypeBishop])
    threats_orthogonal = set([TypeQueen, TypeRook])

    @staticmethod
    def getMoves(piece, position, squares):
        """One square in each direction"""
        position_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue

                x, y = position[0] + i, position[1] + j
                if max(x, y) > 7 or min(x, y) < 0:
                    continue

                o = squares[x][y].piece
                if o and o.is_black != piece.is_black:
                    position_list.append((x, y))
                elif not o:
                    position_list.append((x, y))

        moves = [PieceMove((position, p)) for p in position_list]

        # castling
        if piece.moves_count == 0:
            # castling - short
            rook = squares[7][0].piece
            if rook and rook.type == TypeRook and rook.moves_count == 0:
                free_pass = True
                for i in [5, 6]:
                    if squares[i][0].piece:
                        free_pass = False
                        break

                if free_pass:
                    moves.append(PieceMove(
                        (position, (6, 0)),
                        ((7, 0), (5, 0))
                    ))

            # castling - long
            rook = squares[0][0].piece
            if rook and rook.type == TypeRook and rook.moves_count == 0:
                free_pass = True
                for i in range(1, 4):
                    if squares[i][0].piece:
                        free_pass = False
                        break

                if free_pass:
                    moves.append(PieceMove(
                        (position, (2, 0)),
                        ((0, 0), (3, 0))
                    ))

        return moves

    @staticmethod
    def checkSafe(position, squares):
        king = squares[position[0]][position[1]].piece
        if king.type is not TypeKing:
            raise ValueError('Invalid king position')
        if king.position != position:
            raise ValueError('Invalid king position data! ' + str(position) + ' vs ' + str(king.position))
        king_is_black = king.is_black

        # check diagonals + orthogonals
        for i in range(-1, 2):
            for j in range(-1, 2):
                for d in range(1, 8):
                    x, y = position[0] + i * d, position[1] + j * d

                    # stay on board
                    if max(x, y) > 7 or min(x, y) < 0:
                        break

                    o = squares[x][y].piece
                    if o:
                        if o.is_black == king_is_black:
                            # friendly piece, no threat from this direction
                            break
                        elif d == 1 and o.type == TypeKing:
                            return False
                        elif o.type in TypeKing.threats_diagonal and abs(i) == abs(j):
                            return False
                        elif o.type in TypeKing.threats_orthogonal and abs(i) != abs(j):
                            return False
                        else:
                            # non threatening foe
                            break

        # check knights
        knight_offsets = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for offset in knight_offsets:
            x, y = position[0] + offset[0], position[1] + offset[1]

            # stay on board
            if max(x, y) > 7 or min(x, y) < 0:
                continue

            o = squares[x][y].piece
            if o and o.type == TypeKnight and o.is_black != king_is_black:
                return False

        # check pawns
        if king_is_black:
            pawns_offsets = [(1, -1), (-1, -1)]
        else:
            pawns_offsets = [(1, 1), (-1, 1)]

        for offset in pawns_offsets:
            x, y = position[0] + offset[0], position[1] + offset[1]

            # stay on board
            if max(x, y) > 7 or min(x, y) < 0:
                continue

            o = squares[x][y].piece
            if o and o.type == TypePawn and o.is_black != king_is_black:
                return False

        return True

    @staticmethod
    def checkSafeAfterMove(move, board):
        start_pos = move.moves[0][0]
        end_pos = move.moves[0][1]
        piece = board.squares[start_pos[0]][start_pos[1]].piece

        # init king color and position
        if piece.type is TypeKing:
            kingpos = end_pos
        elif piece.is_black:
            kingpos = board.black_king_pos
        else:
            kingpos = board.white_king_pos

        # no king on board
        if kingpos is None:
            return True

        # fake move
        backup = OrderedDict()
        backup_type = piece.type
        for m in move.moves:
            _from = m[0]
            _to = m[1]

            #backup pieces
            p = board.squares[_from[0]][_from[1]].piece
            backup[(_to[0], _to[1])] = board.squares[_to[0]][_to[1]].piece
            backup[(_from[0], _from[1])] = p

            p.position = _to
            board.squares[_to[0]][_to[1]].piece = p
            board.squares[_from[0]][_from[1]].piece = None

        if move.transformation:
            trans_pos = move.transformation[0]
            trans_piece = board.squares[trans_pos[0]][trans_pos[1]].piece
            if trans_piece:
                trans_piece.type = move.transformation[1]

        # check kings safety
        result = TypeKing.checkSafe(kingpos, board.squares)

        # revert move
        for pos, p in reversed(backup.items()):
            board.squares[pos[0]][pos[1]].piece = p
            if p:
                p.position = pos

        piece.type = backup_type

        # done
        return result


types_dict.load()
