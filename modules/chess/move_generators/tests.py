import unittest

from . import gen_minimax
from .. import board, game


class MinimaxMoveGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.generator = gen_minimax.minimaxGenerator

        self.board = board.Board()
        self.game = game.Game(self.board)

        self.game.init_new()
        self.game.strip()

    def test_1Level(self):
        self.game.initPiece(self.game.piece_list['WK'], (4, 0))
        self.game.initPiece(self.game.piece_list['BK'], (4, 7))

        self.game.initPiece(self.game.piece_list['Wp1'], (3, 3))
        self.game.initPiece(self.game.piece_list['Bp1'], (4, 4))

        move = self.generator(self.game, 1)
        self.assertEquals(move.moves[0][1], (4, 4))

    def test_2Levels(self):
        self.game.initPiece(self.game.piece_list['WK'], (4, 0))
        self.game.initPiece(self.game.piece_list['BK'], (4, 7))

        self.game.initPiece(self.game.piece_list['WQ'], (3, 3))
        self.game.initPiece(self.game.piece_list['Bp1'], (4, 4))
        self.game.initPiece(self.game.piece_list['Bp2'], (5, 5))

        move = self.generator(self.game, 2)
        self.assertNotEquals(move.moves[0][1], (4, 4))
