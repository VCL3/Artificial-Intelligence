from konane import *
from random import random, randrange

class MinimaxNode(object):
    def __init__(self, state, move, depth, player):
        self.state = state
        self.move = move
        self.depth = depth
        self.player = player

class MinimaxPlayer(Konane, Player):
    def __init__(self, size, depthLimit, verbose=False):
        Konane.__init__(self, size) # construct the game
        Player.__init__(self)       # construct the player
        self.limit = depthLimit     # cutoff level of search 
        self.verbose = verbose      # flag used to view debugging messages
        self.bestScore = 1000       # best possible score for maximizer
        self.worstScore = -1000     # worst possible score for maximizer

    def initialize(self, side):
        self.name = "MinimaxPlayerDepth" + str(self.limit)
        self.side = side

    def getMove(self, board):
        moves = self.generateMoves(board, self.side)
        root_node = MinimaxNode(board, None, 0, self.side)
        return self.boundedMinimax(root_node)

    def eval(self, node):
        black_moves = self.generateMoves(node.state, 'B')
        white_moves = self.generateMoves(node.state, 'W')
        black_number = len(black_moves)
        if black_number == 0:
            return self.worstScore
        white_number = len(white_moves)
        if white_number == 0:
            return self.bestScore
        return black_number - white_number

    def boundedMinimax(self, node):
        values = []
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0:
            return None
        for move in moves:
            nextState = self.nextBoard(node.state, node.player, move)
            next_node = MinimaxNode(nextState, move, node.depth+1, self.opponent(node.player))
            values.append(self.minValue(next_node))
        max_value = max(values)
        max_index = values.index(max_value)
        return moves[max_index]

    def minValue(self, node):
        if node.depth == self.limit:
            return self.eval(node)
        moves = self.generateMoves(node.state, node.player)
        if len(moves) == 0 :
            return self.eval(node)
        v = self.bestScore
        for move in moves:
            nextState = self.nextBoard(node.state, node.player, move)
            next_node = MinimaxNode(nextState, move, node.depth+1, self.opponent(node.player))
            v = min(v, maxValue(next_node))
        return v

    def maxValue(self, node):
        pass

if __name__ == '__main__':
    game = Konane(6)
    game.playOneGame(MinimaxPlayer(6, 4, True), RandomPlayer(6))



