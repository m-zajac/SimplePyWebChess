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
        for i in range(7):
            self.assertEqual(len(squares[i]), 8)
            for j in range(7):
                # is square
                self.assertIsInstance(squares[i][j], board.Square)
                # square piece isn't present
                self.assertIsNone(squares[i][j].piece)


class PieceTests(unittest.TestCase):
    """Piece testing class"""
    def setUp(self):
        self.piece = pieces.Piece(pieces.TypeKing)
        self.board = board.Board()


    def test_moves(self):
        # move list from center of the board
        pos = (4,4)
        
        # King - 1 square each direction == 8
        self.piece.type = pieces.TypeKing
        positions = self.piece.getMoves(pos)
        self.assertEqual(len(positions), 8)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))

            p = map(operator.sub, pos, p)
            self.assertLessEqual(abs(complex(p[0], p[1])), 1.5)
            self.assertGreaterEqual(abs(complex(p[0], p[1])), 0.0)


        # Queen - 1+ square in 8 directions
        self.piece.type = pieces.TypeQueen
        positions = self.piece.getMoves(pos)
        for p in positions:
            self.assertTrue(self.board.onBoard(p))
            self.assertNotIn(p, [(2, 3), (3, 2), (5, 1), (5, 6), (5, 7), (6, 1)])





if __name__ == '__main__':
    unittest.main()
