import copy
import types

from modules.searchtree import nodes


def minimaxGenerator(game, level=1):
    """Minimax move generator
    """
    if game.black_moves:
        init_node = nodes.MinABNode()
    else:
        init_node = nodes.MaxABNode()

    _genTreeLevel(init_node, game, level)

    init_node.traverse()

    return init_node.data


def _make_evaluation_function(game):
    """Node doEvaluate method factory
    """
    def evf(self):
        self.value = _evaluateGame(game)

    return evf


def _genTreeLevel(node, game, stoplevel, first_call=True):
    if stoplevel <= 0:
        return node

    node.doEvaluate = types.MethodType(
        _make_evaluation_function(game),
        node
    )

    if game.black_moves:
        pieces = game.black_pieces
    else:
        pieces = game.white_pieces

    if isinstance(node, nodes.MinABNode):
        node_class = nodes.MaxABNode
    else:
        node_class = nodes.MinABNode

    for piece in pieces:
        for move in piece.getMoves(game.board):
            new_game = copy.deepcopy(game)
            new_game.move(move)

            new_node = node_class()
            node.addNode(new_node)

            if first_call:
                # store move to check
                new_node.move = move
            else:
                # propagate move to the bottom of the tree
                new_node.move = node.move

            if stoplevel == 1:
                # at the bottom - data is the move from first level
                new_node.data = new_node.move
                new_node.doEvaluate = types.MethodType(
                    _make_evaluation_function(new_game),
                    new_node
                )
            else:
                # gen next tree level
                _genTreeLevel(
                    new_node,
                    new_game,
                    stoplevel - 1,
                    first_call=False
                )


def _evaluateGame(game):
    """Evaluates score - for white player
    """
    def red_func(value, piece):
        return value + piece.type.value

    value = reduce(red_func, game.white_pieces, 0)
    value -= reduce(red_func, game.black_pieces, 0)

    return value
