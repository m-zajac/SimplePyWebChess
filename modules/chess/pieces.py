"""Pieces module"""


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

        # format: tuple - (piece, type)
        # params:
        #   piece: instance of Piece
        #   type: TypeQueen, TypeRook ...
        self.transformation = None

    def rotate(self):
        """Transforms coordinates to other player"""
        self.moves = map(lambda m: ((7-m[0][0], 7-m[0][1]), (7-m[1][0], 7-m[1][1])), self.moves)


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
        if self.is_black:
            moves = self.type.getMoves(self, (7 - self.position[0], 7 - self.position[1]), board.squares_reversed)
            map(lambda m: m.rotate(), moves)
        else:
            moves = self.type.getMoves(self, self.position, board.squares)

        # filter by kings safety
        moves = filter(lambda m: Piece.checkKingSafeAfterMove(m, board), moves)
        return moves

    @staticmethod
    def checkKingSafeAfterMove(move, board):
        # init threat data
        if not hasattr(Piece, 'king_threats_diagonal'):
            Piece.king_threats_diagonal = set([TypeQueen, TypeBishop])
            Piece.king_threats_orthogonal = set([TypeRook])

        start_pos = move.moves[0][0]
        end_pos = move.moves[0][1]
        piece = board.squares[start_pos[0]][start_pos[1]].piece

        # do not check for kings move
        if piece.type == TypeKing:
            return True

        # init king color and position
        if piece.is_black:
            kingblack = True
            kingpos = board.black_king_pos
        else:
            kingblack = False
            kingpos = board.white_king_pos

        # no king on board
        if kingpos is None:
            return True

        # check diagonals + orthogonals
        for i in range(-1, 2):
            for j in range(-1, 2):
                for d in range(1, 8):
                    x, y = kingpos[0]+i*d, kingpos[1]+j*d

                    if max(x, y) > 7 or min(x, y) < 0:
                        break

                    # if it's end position of move, this direction is safe
                    if x == end_pos[0] and y == end_pos[1]:
                        break

                    # if it's start position of move, skip this square
                    if x == start_pos[0] and y == start_pos[1]:
                        continue

                    o = board.squares[x][y].piece
                    if o:
                        if o.is_black == kingblack:
                            # friendly piece, no threat from this direction
                            break
                        elif o.type in Piece.king_threats_diagonal and abs(i) == abs(j):
                            return False
                        elif o.type in Piece.king_threats_orthogonal and abs(i) != abs(j):
                            return False
                        else:
                            # non threatening foe
                            break

        return True

    def __eq__(self, other):
        return self.id == other.id and self.type == other.type and self.is_black == other.is_black

    def __str__(self):
        name = 'Black' if self.is_black else 'White'
        name += ' ' + self.id + ' (' + str(self.moves_count) + ' moves)'
        return name


class TypeKing(object):
    """King"""
    @staticmethod
    def getMoves(piece, position, squares):
        """One square in each direction"""
        position_list = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue

                x, y = position[0]+i, position[1]+j
                if max(x, y) > 7 or min(x, y) < 0:
                    continue

                o = squares[x][y].piece
                if o and o.is_black != piece.is_black:
                    position_list.append((x, y))
                elif not o:
                    position_list.append((x, y))

        return [PieceMove((position, p)) for p in position_list]


class TypeBishop(object):
    """Bishop"""
    @staticmethod
    def getMoves(piece, position, squares):
        """One+ square in each diagonal direction"""
        position_list = []
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                for d in range(1, 8):
                    x, y = position[0]+i*d, position[1]+j*d

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
    @staticmethod
    def getMoves(piece, position, squares):
        """Horizontal + vertical moves"""
        position_list = []
        for i in range(4):
            for d in range(1, 8):
                if i == 0:
                    x, y = position[0]+d, position[1]
                elif i == 1:
                    x, y = position[0]-d, position[1]
                elif i == 2:
                    x, y = position[0], position[1] + d
                else:
                    x, y = position[0], position[1]-d

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
    @staticmethod
    def getMoves(piece, position, squares):
        return TypeRook.getMoves(piece, position, squares) + TypeBishop.getMoves(piece, position, squares)


class TypeKnight(object):
    """Knight"""
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
    @staticmethod
    def getMoves(piece, position, squares):
        position_list = []
        offsets = [(0, 1)]
        # if first move - may be 2 squares
        if piece.moves_count == 0 and position[1] == 1:
            offsets.append((0, 2))

        for offset in offsets:
            x, y = position[0] + offset[0], position[1] + offset[1]

            if max(x, y) > 7 or min(x, y) < 0:
                continue

            # if first offset is blocked - there are no more normal moves
            if squares[x][y].piece:
                break

            position_list.append((x, y))

        # check attacks
        attacks = [(1, 1), (-1, 1)]
        for attack in attacks:
            x, y = position[0] + attack[0], position[1] + attack[1]

            if max(x, y) > 7 or min(x, y) < 0:
                continue

            o = squares[x][y].piece
            if not o or o.is_black == piece.is_black:
                continue

            position_list.append((x, y))

        return [PieceMove((position, p)) for p in position_list]
