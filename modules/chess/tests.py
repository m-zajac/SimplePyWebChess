"""Chess tests"""
import unittest
import operator
import json
import board
import pieces
import game


class BoardTests(unittest.TestCase):
    """Board testing class"""
    def setUp(self):
        self.board = board.Board()

    def test_board(self):
        # board size, check squares
        self.assertIsInstance(self.board.squares, list)
        self.assertEqual(len(self.board.squares), 8)

        self.assertTrue(self.board.squares[0][0].is_black)
        self.assertTrue(self.board.squares[4][4].is_black)

        self.assertFalse(self.board.squares[7][0].is_black)
        self.assertFalse(self.board.squares[4][3].is_black)

        self.assertEqual(self.board.squares[0][0], self.board.squares_reversed[7][7])
        self.assertEqual(self.board.squares[1][1], self.board.squares_reversed[6][6])

        for i in range(7):
            self.assertEqual(len(self.board.squares[i]), 8)
            for j in range(7):
                # is square
                self.assertIsInstance(self.board.squares[i][j], board.Square)
                # square piece isn't present
                self.assertIsNone(self.board.squares[i][j].piece)
                # check color
                if (i + j) % 2:
                    self.assertFalse(self.board.squares[i][j].is_black)
                else:
                    self.assertTrue(self.board.squares[i][j].is_black)
                # check reversed
                self.assertEqual(self.board.squares[i][j], self.board.squares_reversed[7-i][7-j], str(i) + ', ' + str(j))

    def test_piece_actions(self):
        board_manager = board.BoardManager

        TestPiece1 = pieces.Piece(pieces.TypePawn, False, 'WP1')
        piecePos1 = (4, 3)
        board_manager.initPiece(self.board, TestPiece1, piecePos1)
        TestPiece1.moves_count = 1

        TestPiece2 = pieces.Piece(pieces.TypePawn, True, 'BP1')
        piecePos2 = (4, 5)
        board_manager.initPiece(self.board, TestPiece2, piecePos2)
        TestPiece2.moves_count = 1

        # test count
        white_pieces = []
        black_pieces = []
        for row in self.board.squares:
            for square in row:
                if square.piece:
                    if square.piece.is_black:
                        black_pieces.append(square.piece)
                    else:
                        white_pieces.append(square.piece)

        self.assertEqual(len(white_pieces), 1)
        self.assertEqual(len(black_pieces), 1)

        # test board squares
        self.assertEqual(self.board.squares[4][3].piece, TestPiece1)
        self.assertEqual(self.board.squares_reversed[3][4].piece, TestPiece1)
        self.assertEqual(self.board.squares[4][5].piece, TestPiece2)
        self.assertEqual(self.board.squares_reversed[3][2].piece, TestPiece2)

        # test remove
        board_manager.removePiece(self.board, TestPiece2)
        self.assertIsNone(TestPiece2.position)


class PawnTests(unittest.TestCase):
    """Pawn testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_moves(self):
        # init white
        TestPieceW = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, TestPieceW, (0, 1))

        # init black
        TestPieceB = pieces.Piece(pieces.TypePawn, True)
        self.board_manager.initPiece(self.board, TestPieceB, (0, 6))

        # check initial 2 moves
        movelistW = TestPieceW.getMoves(self.board)
        self.assertEqual(len(movelistW), 2)
        self.assertEqual(movelistW[0].moves[0][1], (0, 2))
        self.assertEqual(movelistW[1].moves[0][1], (0, 3))

        movelistB = TestPieceB.getMoves(self.board)
        self.assertEqual(len(movelistB), 2)
        self.assertEqual(movelistB[0].moves[0][1], (0, 5))
        self.assertEqual(movelistB[1].moves[0][1], (0, 4))

        # move 2 squares
        self.board_manager.move(self.board, movelistW[1])
        self.assertEqual(TestPieceW.position, (0, 3))

        self.board_manager.move(self.board, movelistB[1])
        self.assertEqual(TestPieceB.position, (0, 4))

        # no moves left
        movelistW = TestPieceW.getMoves(self.board)
        movelistB = TestPieceB.getMoves(self.board)
        self.assertEqual(len(movelistW), 0)
        self.assertEqual(len(movelistB), 0)

    def test_attack(self):
        # init white
        TestPieceW = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, TestPieceW, (3, 2))

        # init black
        TestPieceB = pieces.Piece(pieces.TypePawn, True)
        self.board_manager.initPiece(self.board, TestPieceB, (4, 3))

        # test moves
        movelistW = TestPieceW.getMoves(self.board)
        self.assertEqual(len(movelistW), 2)
        self.assertEqual(movelistW[0].moves[0][1], (3, 3))
        self.assertEqual(movelistW[1].moves[0][1], TestPieceB.position)

        movelistB = TestPieceB.getMoves(self.board)
        self.assertEqual(len(movelistB), 2)
        self.assertEqual(movelistB[0].moves[0][1], (4, 2))
        self.assertEqual(movelistB[1].moves[0][1], TestPieceW.position)

    def test_move2squares_blocked(self):
        # init white
        TestPieceW = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, TestPieceW, (0, 1))

        # init black
        TestPieceB = pieces.Piece(pieces.TypePawn, True)
        self.board_manager.initPiece(self.board, TestPieceB, (0, 2))

        # test moves
        movelistW = TestPieceW.getMoves(self.board)
        self.assertEqual(len(movelistW), 0)

    def test_blocked(self):
        # init white
        TestPieceW = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, TestPieceW, (0, 7))

        # test moves
        movelistW = TestPieceW.getMoves(self.board)
        self.assertEqual(len(movelistW), 0)


class KingTests(unittest.TestCase):
    """King testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_moves(self):
        TestPiece = pieces.Piece(pieces.TypeKing, False)
        self.board_manager.initPiece(self.board, TestPiece, (4, 4))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 8)
        for move in movelists:
            p = map(operator.sub, (4, 4), move.moves[0][1])
            self.assertLessEqual(abs(complex(p[0], p[1])), 1.5)
            self.assertGreaterEqual(abs(complex(p[0], p[1])), 0.0)

    def test_blocked(self):
        TestPiece = pieces.Piece(pieces.TypeKing, False)
        self.board_manager.initPiece(self.board, TestPiece, (0, 0))

        O1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O1, (1, 0))
        O2 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O2, (1, 1))
        O3 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O3, (0, 1))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 0)


class QueenTests(unittest.TestCase):
    """Queen testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_moves(self):
        TestPiece = pieces.Piece(pieces.TypeQueen, False)
        self.board_manager.initPiece(self.board, TestPiece, (4, 4))

        movelists = TestPiece.getMoves(self.board)
        for move in movelists:
            self.assertNotIn(move.moves[0][1], [(2, 3), (3, 2), (5, 1), (5, 6), (5, 7), (6, 1)])

    def test_blocked(self):
        TestPiece = pieces.Piece(pieces.TypeQueen, False)
        self.board_manager.initPiece(self.board, TestPiece, (0, 0))

        O1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O1, (1, 0))
        O2 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O2, (1, 1))
        O3 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O3, (0, 1))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 0)

    def test_blocked2(self):
        TestPiece = pieces.Piece(pieces.TypeQueen, False)
        self.board_manager.initPiece(self.board, TestPiece, (3, 0))

        P1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, P1, (3, 1))
        P2 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, P2, (2, 1))
        B = pieces.Piece(pieces.TypeBishop, False)
        self.board_manager.initPiece(self.board, B, (2, 0))
        K = pieces.Piece(pieces.TypeKing, False)
        self.board_manager.initPiece(self.board, K, (4, 0))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 4)


class BishopTests(unittest.TestCase):
    """Bishop testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_moves(self):
        TestPiece = pieces.Piece(pieces.TypeBishop, False)
        self.board_manager.initPiece(self.board, TestPiece, (4, 4))

        movelists = TestPiece.getMoves(self.board)
        for move in movelists:
            # same square color after move
            self.assertTrue(self.board.squares[move.moves[0][1][0]][move.moves[0][1][1]].is_black == self.board.squares[4][4].is_black)
            # only diagonal
            delta = (move.moves[0][1][0] - 4, move.moves[0][1][1] - 4)
            self.assertTrue(abs(delta[0]) == abs(delta[1]))

    def test_blocked(self):
        TestPiece = pieces.Piece(pieces.TypeBishop, False)
        self.board_manager.initPiece(self.board, TestPiece, (0, 0))

        O1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O1, (1, 0))
        O2 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O2, (1, 1))
        O3 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O3, (0, 1))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 0)


class KnightTests(unittest.TestCase):
    """Knight testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_moves(self):
        TestPiece = pieces.Piece(pieces.TypeKnight, False)
        self.board_manager.initPiece(self.board, TestPiece, (4, 4))

        movelists = TestPiece.getMoves(self.board)
        for move in movelists:
            # different color after move
            self.assertFalse(self.board.squares[move.moves[0][1][0]][move.moves[0][1][1]].is_black == self.board.squares[4][4].is_black)
            # L
            delta = (move.moves[0][1][0] - 4, move.moves[0][1][1] - 4)
            self.assertIn(delta, [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])

    def test_nonblocked(self):
        TestPiece = pieces.Piece(pieces.TypeKnight, False)
        self.board_manager.initPiece(self.board, TestPiece, (0, 0))

        O1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O1, (1, 0))
        O2 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O2, (1, 1))
        O3 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, O3, (0, 1))

        movelists = TestPiece.getMoves(self.board)
        self.assertEqual(len(movelists), 2)


class KingSafetyTests(unittest.TestCase):
    """King safety testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager

    def test_1(self):
        """White Pawn can't move"""
        WK = pieces.Piece(pieces.TypeKing, False)
        self.board_manager.initPiece(self.board, WK, (0, 0))

        WP1 = pieces.Piece(pieces.TypePawn, False)
        self.board_manager.initPiece(self.board, WP1, (1, 1))

        BQ = pieces.Piece(pieces.TypeQueen, True)
        self.board_manager.initPiece(self.board, BQ, (7, 7))

        movelists = WP1.getMoves(self.board)
        self.assertEqual(len(movelists), 0)

    def test_2(self):
        """White queen has to cover the king - only one move available"""
        WK = pieces.Piece(pieces.TypeKing, False)
        self.board_manager.initPiece(self.board, WK, (0, 0))

        WQ = pieces.Piece(pieces.TypeQueen, False)
        self.board_manager.initPiece(self.board, WQ, (1, 0))

        BQ = pieces.Piece(pieces.TypeQueen, True)
        self.board_manager.initPiece(self.board, BQ, (7, 7))

        movelists = WQ.getMoves(self.board)
        self.assertEqual(len(movelists), 1)


class GameTests(unittest.TestCase):
    """Game testing class"""
    def setUp(self):
        self.board = board.Board()
        self.board_manager = board.BoardManager
        self.game = game.Game(self.board)

    def test_setup(self):
        self.game.init_new()

        white_pieces = []
        black_pieces = []
        for row in self.board.squares:
            for square in row:
                if square.piece:
                    if square.piece.is_black:
                        black_pieces.append(square.piece)
                    else:
                        white_pieces.append(square.piece)

        self.assertEqual(len(white_pieces), 16)
        self.assertEqual(len(black_pieces), 16)

        self.assertIs(self.board.squares[0][0].piece.type, pieces.TypeRook)
        self.assertFalse(self.board.squares[0][0].piece.is_black)

        self.assertIs(self.board.squares[7][7].piece.type, pieces.TypeRook)
        self.assertTrue(self.board.squares[7][7].piece.is_black)

        self.assertIs(self.board.squares[4][0].piece.type, pieces.TypeKing)
        self.assertFalse(self.board.squares[4][0].piece.is_black)

        self.assertIs(self.board.squares[3][7].piece.type, pieces.TypeQueen)
        self.assertTrue(self.board.squares[3][7].piece.is_black)

        for i in range(8):
            for j in range(2):
                self.assertIsNotNone(self.board.squares[i][j].piece)
                self.assertIsNotNone(self.board.squares[i][7-j].piece)

            for j in range(2, 5):
                self.assertIsNone(self.board.squares[i][j].piece)
                self.assertIsNone(self.board.squares[i][7-j].piece)

    def test_board_serialization(self):
        self.game.init_new()

        serialized = self.board_manager.serialize(self.board)
        serialized = json.dumps(serialized, separators=(',', ':'))

        data = json.loads(serialized)
        newboard = board.Board()
        self.board_manager.deserialize(newboard, data)

        self.assertEqual(newboard.squares, self.board.squares)

    def test_game(self):
        """http://en.wikibooks.org/wiki/Chess/Sample_chess_game"""
        self.game.init_new()

        # w pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 1), (4, 3))),
            black_moves=True,
            is_capture=False,
            white_capture_count=0,
            black_capture_count=0,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 6), (4, 4))),
            black_moves=False,
            is_capture=False,
            white_capture_count=0,
            black_capture_count=0,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w bishop
        self.move_and_checkafter(
            move=pieces.PieceMove(((6, 0), (5, 2))),
            black_moves=True,
            is_capture=False,
            white_capture_count=0,
            black_capture_count=0,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 6), (5, 5))),
            black_moves=False,
            is_capture=False,
            white_capture_count=0,
            black_capture_count=0,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w knight captures b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 2), (4, 4))),
            black_moves=True,
            is_capture=True,
            white_capture_count=1,
            black_capture_count=0,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b pawn captures white bishop
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 5), (4, 4))),
            black_moves=False,
            is_capture=True,
            white_capture_count=1,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w queen - check!
        self.move_and_checkafter(
            move=pieces.PieceMove(((3, 0), (7, 4))),
            black_moves=True,
            is_capture=False,
            white_capture_count=1,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b king
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 7), (4, 6))),
            black_moves=False,
            is_capture=False,
            white_capture_count=1,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w queen - capture & check!
        self.move_and_checkafter(
            move=pieces.PieceMove(((7, 4), (4, 4))),
            black_moves=True,
            is_capture=True,
            white_capture_count=2,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b king
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 6), (5, 6))),
            black_moves=False,
            is_capture=False,
            white_capture_count=2,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w bishop - check
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 0), (2, 3))),
            black_moves=True,
            is_capture=False,
            white_capture_count=2,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((3, 6), (3, 4))),
            black_moves=False,
            is_capture=False,
            white_capture_count=2,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w bishop - capture & check
        self.move_and_checkafter(
            move=pieces.PieceMove(((2, 3), (3, 4))),
            black_moves=True,
            is_capture=True,
            white_capture_count=3,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b king
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 6), (6, 5))),
            black_moves=False,
            is_capture=False,
            white_capture_count=3,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((7, 1), (7, 3))),
            black_moves=True,
            is_capture=False,
            white_capture_count=3,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((7, 6), (7, 4))),
            black_moves=False,
            is_capture=False,
            white_capture_count=3,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w bishop - capture pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((3, 4), (1, 6))),
            black_moves=True,
            is_capture=True,
            white_capture_count=4,
            black_capture_count=1,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b bishop
        self.move_and_checkafter(
            move=pieces.PieceMove(((2, 7), (1, 6))),
            black_moves=False,
            is_capture=True,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w queen
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 4), (5, 4))),
            black_moves=True,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b king
        self.move_and_checkafter(
            move=pieces.PieceMove(((6, 5), (7, 5))),
            black_moves=False,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=True,
            black_king_pos=(7, 5),
            white_king_pos=(4, 0),
        )
        # w pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((3, 1), (3, 3))),
            black_moves=True,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=False,
        )
        # b pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((6, 6), (6, 4))),
            black_moves=False,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=True,
        )
        # w queen
        self.move_and_checkafter(
            move=pieces.PieceMove(((5, 4), (5, 6))),
            black_moves=True,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=True,
        )
        # b queen
        self.move_and_checkafter(
            move=pieces.PieceMove(((3, 7), (4, 6))),
            black_moves=False,
            is_capture=False,
            white_capture_count=4,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=True,
            black_king_pos=(7, 5),
            white_king_pos=(4, 0),
        )
        # w pawn
        self.move_and_checkafter(
            move=pieces.PieceMove(((7, 3), (6, 4))),
            black_moves=True,
            is_capture=True,
            white_capture_count=5,
            black_capture_count=2,
            white_king_safe=True,
            black_king_safe=False,
            black_king_pos=(7, 5),
            white_king_pos=(4, 0),
        )
        # b queen
        self.move_and_checkafter(
            move=pieces.PieceMove(((4, 6), (6, 4))),
            black_moves=False,
            is_capture=True,
            white_capture_count=5,
            black_capture_count=3,
            white_king_safe=True,
            black_king_safe=True,
            black_king_pos=(7, 5),
            white_king_pos=(4, 0),
        )
        # w rook - chekcmate
        self.move_and_checkafter(
            move=pieces.PieceMove(((7, 0), (7, 4))),
            black_moves=True,
            is_capture=True,
            white_capture_count=6,
            black_capture_count=3,
            white_king_safe=True,
            black_king_safe=False,
            black_king_pos=(7, 5),
            white_king_pos=(4, 0),
            checkmate=True
        )

    def move_and_checkafter(
        self,
        move,
        black_moves,
        is_capture,
        white_capture_count,
        black_capture_count,
        white_king_safe=True,
        black_king_safe=True,
        white_king_pos=None,
        black_king_pos=None,
        checkmate=None
    ):
        captures = self.game.move(move)
        self.assertEqual(len(captures) > 0, is_capture)
        if len(captures) > 0:
            self.assertEqual(captures[0].is_black, black_moves)

        self.assertEqual(len(self.game.white_captures), white_capture_count)
        self.assertEqual(len(self.game.black_captures), black_capture_count)

        self.assertEqual(pieces.TypeKing.checkSafe(self.game.board.white_king_pos, self.game.board.squares), white_king_safe)
        self.assertEqual(pieces.TypeKing.checkSafe(self.game.board.black_king_pos, self.game.board.squares), black_king_safe)

        self.assertEqual(black_moves, self.game.black_moves)

        if white_king_pos:
            self.assertEqual(self.game.board.white_king_pos, white_king_pos)
            self.assertIs(self.game.board.squares[white_king_pos[0]][white_king_pos[1]].piece.type, pieces.TypeKing)
            self.assertEqual(self.game.board.squares[white_king_pos[0]][white_king_pos[1]].piece.position, white_king_pos)
        if black_king_pos:
            self.assertEqual(self.game.board.black_king_pos, black_king_pos)
            self.assertIs(self.game.board.squares[black_king_pos[0]][black_king_pos[1]].piece.type, pieces.TypeKing)
            self.assertEqual(self.game.board.squares[black_king_pos[0]][black_king_pos[1]].piece.position, black_king_pos)
        if checkmate:
            self.assertEqual(len(self.game.getAllMoves()), 0)
