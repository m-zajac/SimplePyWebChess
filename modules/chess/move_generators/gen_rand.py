import random


def randomGenerator(game):
    """Random move generator
    """
    def getRandomPieceMoves():
        if game.black_moves:
            piece = random.choice(game.black_pieces)
        else:
            piece = random.choice(game.white_pieces)

        return piece.getMoves(game.board)

    moves = []
    while len(moves) == 0:
        moves = getRandomPieceMoves()

    if len(moves) > 0:
        return random.choice(moves)

    return None
