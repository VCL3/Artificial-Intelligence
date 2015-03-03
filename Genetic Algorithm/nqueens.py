
from random import *

class NQueens:
    """
    This class can be used to represent instances of the N-Queens
    problem.  In this problem N Queens must be placed on an NxN board
    in such a way that no Queen can attack another.  Queens can move
    horizontally, vertically, or diagonally.

    The board is represented as an NxN array of booleans, where True
    indicates the location of a Queen.  The Queens are initially
    placed in unique rows.  
    """
    def __init__(self, colPosition=None, n=8):
        """
        Use the given column positions for each row to generate a board.
        For example, board = NQueens([0,1,2,3]), would create a board with
        queens along the diagonal.

        Or generate a randomly configured board with one queen in each row.
        For example, board = NQueens(4), would create a randome board with
        a queen in each row.  
        """
        if colPosition != None:
            self.n = len(colPosition)
            self.board = [[False for c in range(self.n)] \
                          for r in range(self.n)]
            for r in range(self.n):
                self.board[r][colPosition[r]] = True
        else:
            self.n = n
            self.board = [[False for c in range(n)] for r in range(n)]
            for i in range(n):
                self.board[i][randint(0,n-1)] = True
    def __str__(self):
        result = ""
        result += ("-" * ((self.n*2)+1)) + "\n"
        for i in range(self.n):
            result += "|"
            for j in range(self.n):
                if self.board[i][j] == True:
                    result += 'Q|'
                else:
                    result += ' |'
            result += "\n" 
        result += ("-" * ((self.n*2)+1))
        return result
    def attackingQueens(self, r, c, deltaR, deltaC):
        """
        Starting from the current row r and the current column c, look
        in one direction defined by deltaR and deltaC.  If another queen
        is encountered increment a counter.  
        """
        r += deltaR
        c += deltaC
        count = 0
        while r>=0 and r<self.n and c>=0 and c<self.n:
            if self.board[r][c]:
                 count += 1
            r += deltaR
            c += deltaC
        return count
    def allAttacks(self):
        """
        Returns the number of pairs of attacking queens on the board.
        """
        count = 0
        for r in range(self.n):
            c = self.board[r].index(True)
            count += self.attackingQueens(r, c, 1, 0)
            count += self.attackingQueens(r, c, -1, 0)
            count += self.attackingQueens(r, c, 1, 1)
            count += self.attackingQueens(r, c, 1, -1)
            count += self.attackingQueens(r, c, -1, -1)
            count += self.attackingQueens(r, c, -1, 1)
        return count/2
    def safeDirection(self, r, c, deltaR, deltaC):
        """
        Starting from the current row r and the current column c, look
        in one direction defined by deltaR and deltaC.  If another queen
        is encountered return False, otherwise return True.
        """
        r += deltaR
        c += deltaC
        while r>=0 and r<self.n and c>=0 and c<self.n:
            if self.board[r][c]:
                return False
            r += deltaR
            c += deltaC
        return True
    def safeQueens(self):
        """
        Returns the number of safe queens on the board.
        """
        count = 0
        for r in range(self.n):
            c = self.board[r].index(True)
            if (self.safeDirection(r, c, 1, 0) and
                self.safeDirection(r, c, -1, 0) and
                self.safeDirection(r, c, 1, 1) and
                self.safeDirection(r, c, 1, -1) and
                self.safeDirection(r, c, -1, -1) and
                self.safeDirection(r, c, -1, 1)):
                count += 1
        return count
    def eval(self):
        #Try to minimize number of pairs of queens under attack
        #return self.allAttacks()
        
        #Try to maximize number of safe queens
        return self.safeQueens() 
    def successors(self):
        """
        Successors are created by producing every possible new column
        placement for each queen on the board.
        """
        position = []
        for r in range(self.n):
            position.append(self.board[r].index(True))
        result = []
        for r in range(self.n):
            for c in range(1,self.n):
                position[r] = (position[r]+1) % self.n
                result.append(NQueens(colPosition = position ))
            position[r] = (position[r]+1) % self.n
        return result
    def goalFound(self):
        #Use when trying to minimize pairs of queens under attack
        #return self.eval() == 0
        #Use when trying to maximize number of safe queens
        return self.eval() == self.n
                
if __name__ == '__main__':
    board = NQueens([0,1,2,3,4,5])
    print board
    print "Safe queens:", board.safeQueens()
    board2 = NQueens([0,2,4,1,3,5,6,7])
    print board2
    print "Safe queens:", board2.safeQueens()
    board3 = NQueens([0,1,0,1,0,1,0,1,0,1])
    print board3
    print "Safe queens:", board3.safeQueens()
    
