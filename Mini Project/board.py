from piece import Piece, Empty, Pawn, Rook, Knight, Bishop, Queen, King

'''
pieceType:
    0: empty ('')
    1: pawn ('p')
    2: rook ('r')
    3: knight ('n')
    4: bishop ('b')
    5: queen ('q')
    6: king ('k')
    (lowercase if player, uppercase if opponent)

<CAUTION>
Nested for loops to iterate over "board" needs to be in the form: for y { for x {...}}
to iterate from left to right before moving top to bottom
'''

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        subclasses = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        cnt = 0
        for subclass in subclasses:
            self.board[cnt][0] = subclass(cnt, 0, False)
            self.board[cnt][1] = Pawn(cnt, 1, False)
            self.board[cnt][6] = Pawn(cnt, 6, True)
            self.board[cnt][7] = subclass(cnt, 7, True)
            cnt+=1
        for j in range(2,6):
            for i in range(8):
                self.board[i][j] = Empty(i, j)

    def getBoardStr(self):
        returnBoard = [['' for _ in range(8)] for _ in range(8)]
        for j in range(len(self.board[0])):
            for i in range(len(self.board)):
                returnBoard[i][j] = self.board[i][j].toString()
        return returnBoard

    def getBoardPiece(self):
        return self.board