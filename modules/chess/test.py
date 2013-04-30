"""Chess tests"""
import unittest
import operator
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
                self.assertEqual(self.board.squares[i][j], self.board.squares_reversed[7-j][7-i], str(i) + ', ' + str(j))

    def test_piece_actions(self):
        TestPiece1 = pieces.Piece(pieces.TypePawn, False, 'WP1')
        piecePos1 = (4, 3)
        self.board.initPiece(TestPiece1, piecePos1)

        TestPiece2 = pieces.Piece(pieces.TypePawn, True, 'BP1')
        piecePos2 = (4, 5)
        self.board.initPiece(TestPiece2, piecePos2)

        # test count
        self.assertEqual(len(self.board.white_pieces), 1)
        self.assertEqual(len(self.board.black_pieces), 1)

        # test move and capture
        # move p1 up, to (4, 4)
        moves = TestPiece1.getMoves(piecePos1, self.board)
        self.assertEqual(len(moves), 1)
        self.board.movePiece(TestPiece1, moves[0])
        self.assertTupleEqual(self.board.white_pieces[TestPiece1.id]['pos'], (4, 4))

        # move p2 up and capture
        moves = TestPiece2.getMoves(piecePos2, self.board)
        self.assertEqual(len(moves), 1)
        capture = self.board.movePiece(TestPiece2, moves[0])
        self.assertTupleEqual(self.board.black_pieces[TestPiece2.id]['pos'], (4, 4))
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
        positions = TestPiece.getMoves(pos, self.board)
        self.assertEqual(len(positions), 8)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))

            p = map(operator.sub, pos, p)
            self.assertLessEqual(abs(complex(p[0], p[1])), 1.5)
            self.assertGreaterEqual(abs(complex(p[0], p[1])), 0.0)

        # Queen - 1+ square in 8 directions
        TestPiece.type = pieces.TypeQueen
        positions = TestPiece.getMoves(pos, self.board)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            self.assertNotIn(p, [(2, 3), (3, 2), (5, 1), (5, 6), (5, 7), (6, 1)])

        # Bishop - diagonal
        TestPiece.type = pieces.TypeBishop
        positions = TestPiece.getMoves(pos, self.board)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            # same color after move
            self.assertTrue(self.board.squares[p[0]][p[1]].is_black == self.board.squares[pos[0]][pos[1]].is_black)
            # only diagonal
            delta = (p[0] - pos[0], p[1] - pos[1])
            self.assertTrue(abs(delta[0]) == abs(delta[1]))

        # Knight - L moves
        TestPiece.type = pieces.TypeKnight
        positions = TestPiece.getMoves(pos, self.board)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            # different color after move
            self.assertFalse(self.board.squares[p[0]][p[1]].is_black == self.board.squares[pos[0]][pos[1]].is_black)
            # L
            delta = (p[0] - pos[0], p[1] - pos[1])
            self.assertIn(delta, [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)])

        # Pawn
        # 1 square up
        TestPiece.type = pieces.TypePawn
        positions = TestPiece.getMoves(pos, self.board)
        self.assertTrue(len(positions) == 1)
        self.assertListEqual(positions, [(4, 5)])
        # 2 squares up
        positions = TestPiece.getMoves((4, 1), self.board)
        self.assertTrue(len(positions) == 2)
        self.assertListEqual(positions, [(4, 2), (4, 3)])

    def test_King_moves(self):
        TestPiece = pieces.Piece(pieces.TypeKing, False, 'WKing')
        testPos = (4, 4)
        self.board.initPiece(TestPiece, testPos)

        # other piece, same color
        Obstacle = pieces.Piece(pieces.TypePawn, False, 'WP1')
        obstaclePos = (4, 5)
        self.board.initPiece(Obstacle, obstaclePos)

        positions = TestPiece.getMoves(testPos, self.board)
        self.assertNotIn(obstaclePos, positions)

        # other piece, different color
        Obstacle.is_black = True
        positions = TestPiece.getMoves(testPos, self.board)
        self.assertIn(obstaclePos, positions)


class GameTests(unittest.TestCase):
    """Game testing class"""
    def setUp(self):
        self.board = board.Board()
        self.game = game.Game(self.board)

    def test_setup(self):
        self.game.init_new()

        self.assertEqual(len(self.board.white_pieces), 16)
        self.assertEqual(len(self.board.black_pieces), 16)

        self.assertIs(self.board.squares[0][0].piece.type, pieces.TypeRook)
        self.assertFalse(self.board.squares[0][0].piece.is_black)

        self.assertIs(self.board.squares[7][7].piece.type, pieces.TypeRook)
        self.assertTrue(self.board.squares[7][7].piece.is_black)

        self.assertIs(self.board.squares[4][0].piece.type, pieces.TypeKing)
        self.assertFalse(self.board.squares[4][0].piece.is_black)

        self.assertIs(self.board.squares[3][7].piece.type, pieces.TypeKing)
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

        serialized = self.board.serialize()

        newboard = board.Board()
        newboard.deserialize(serialized)

        self.assertEqual(newboard.white_pieces, self.board.white_pieces)

    def test_game(self):
        self.game.init_new()

        # http://en.wikibooks.org/wiki/Chess/Sample_chess_game
        # w pawn
        self.game.move((4, 1), (4, 3))
        # b pawn
        self.game.move((4, 6), (4, 4))
        # w bishop
        self.game.move((6, 0), (5, 2))
        # b pawn
        self.game.move((5, 6), (5, 5))
        # w knight captures b pawn
        self.game.move((5, 2), (4, 4))
        self.assertIs(self.board.white_captures[0].type, pieces.TypePawn)
        self.assertTrue(self.board.white_captures[0].is_black)
        # b pawn captures white bishop
        self.game.move((5, 5), (4, 4))
        self.assertIs(self.board.black_captures[0].type, pieces.TypeKnight)
        self.assertFalse(self.board.black_captures[0].is_black)
        # w queen - check!
        self.game.move((3, 0), (7, 4))

        # TODO: checks, checkmates
