"""Chess tests"""
import unittest
import operator
import board
import pieces


class BoardTests(unittest.TestCase):
    """Board testing class"""
    def setUp(self):
        self.board = board.Board()

    def test_board(self):
        squares = self.board.squares

        # board size, check squares
        self.assertIsInstance(squares, tuple)
        self.assertEqual(len(squares), 8)

        self.assertTrue(squares[0][0].is_black)
        self.assertTrue(squares[4][4].is_black)

        self.assertFalse(squares[7][0].is_black)
        self.assertFalse(squares[4][3].is_black)

        for i in range(7):
            self.assertEqual(len(squares[i]), 8)
            for j in range(7):
                # is square
                self.assertIsInstance(squares[i][j], board.Square)
                # square piece isn't present
                self.assertIsNone(squares[i][j].piece)
                # check color
                if (i + j) % 2:
                    self.assertFalse(squares[i][j].is_black)
                else:
                    self.assertTrue(squares[i][j].is_black)

    def test_pieces(self):
        TestPiece1 = pieces.Piece(pieces.TypePawn, False, 'WP1')
        piecePos1 = (4, 5)
        self.board.initPiece(TestPiece1, piecePos1)

        TestPiece2 = pieces.Piece(pieces.TypeKing, True, 'BKing')
        piecePos2 = (3, 6)
        self.board.initPiece(TestPiece2, piecePos2)

        # test count
        self.assertEqual(len(self.board.white_pieces), 1)
        self.assertEqual(len(self.board.black_pieces), 1)

        # test move and capture
        pos = (4, 6)
        self.board.movePiece(TestPiece1, pos)
        self.assertTupleEqual(self.board.white_pieces[TestPiece1.id]['pos'], pos)

        pos = (4, 6)
        capture = self.board.movePiece(TestPiece2, pos)
        self.assertTupleEqual(self.board.black_pieces[TestPiece2.id]['pos'], pos)
        self.assertIsInstance(capture, pieces.Piece)
        self.assertEqual(len(self.board.white_pieces), 0)

        # test remove
        self.board.removePiece(TestPiece2)
        self.assertEqual(len(self.board.black_pieces), 0)


class PieceTests(unittest.TestCase):
    """Piece testing class"""
    def setUp(self):
        self.board = board.Board()

    def test_empty_board_moves(self):
        # move list from center of the board
        pos = (4, 4)

        # King - 1 square each direction == 8
        TestPiece = pieces.Piece(pieces.TypeKing, False)
        positions = TestPiece.getMoves(pos, self.board.squares)
        self.assertEqual(len(positions), 8)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))

            p = map(operator.sub, pos, p)
            self.assertLessEqual(abs(complex(p[0], p[1])), 1.5)
            self.assertGreaterEqual(abs(complex(p[0], p[1])), 0.0)

        # Queen - 1+ square in 8 directions
        TestPiece.type = pieces.TypeQueen
        positions = TestPiece.getMoves(pos, self.board.squares)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            self.assertNotIn(p, [(2, 3), (3, 2), (5, 1), (5, 6), (5, 7), (6, 1)])

        # Bishop - diagonal
        TestPiece.type = pieces.TypeBishop
        positions = TestPiece.getMoves(pos, self.board.squares)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            # same color after move
            self.assertTrue(self.board.squares[p[0]][p[1]].is_black == self.board.squares[pos[0]][pos[1]].is_black)
            # only diagonal
            delta = (p[0] - pos[0], p[1] - pos[1])
            self.assertTrue(abs(delta[0]) == abs(delta[1]))

        # Knight - L moves
        TestPiece.type = pieces.TypeKnight
        positions = TestPiece.getMoves(pos, self.board.squares)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            # different color after move
            self.assertFalse(self.board.squares[p[0]][p[1]].is_black == self.board.squares[pos[0]][pos[1]].is_black)
            # L
            delta = (p[0] - pos[0], p[1] - pos[1])
            self.assertIn(delta, [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])

        # Pawn - 1 square up
        TestPiece.type = pieces.TypePawn
        positions = TestPiece.getMoves(pos, self.board.squares)
        self.assertTrue(len(positions) == 1)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            # different color after move
            self.assertFalse(self.board.squares[p[0]][p[1]].is_black == self.board.squares[pos[0]][pos[1]].is_black)
            # 1 up
            delta = (p[0] - pos[0], p[1] - pos[1])
            self.assertEqual(delta, (0, 1))

    def test_King_moves(self):
        TestPiece = pieces.Piece(pieces.TypeKing, False, 'WKing')
        testPos = (4, 4)
        self.board.initPiece(TestPiece, testPos)

        # other piece, same color
        Obstacle = pieces.Piece(pieces.TypePawn, False, 'WP1')
        obstaclePos = (4, 5)
        self.board.initPiece(Obstacle, obstaclePos)

        positions = TestPiece.getMoves(testPos, self.board.squares)
        self.assertNotIn(obstaclePos, positions)

        # other piece, different color
        Obstacle.is_black = True
        positions = TestPiece.getMoves(testPos, self.board.squares)
        self.assertIn(obstaclePos, positions)
