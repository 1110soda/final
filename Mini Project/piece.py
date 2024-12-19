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
'''

class Piece():
    def __init__(self, x, y, changes, pieceType, player):
        #index of piece
        self.x = x
        self.y = y
        #list of index changes (movements) of the piece
        self.changes = changes
        #String version of the piece
        self.pieceType = pieceType
        #True if player, false if opponent
        self.player = player
    
    def toString(self):
        return self.pieceType

    def move(self, endX, endY, boardList): #switch location of the moved piece and the piece/empty at end index
        boardList[endX][endY] = boardList[self.x][self.y]
        boardList[self.x][self.y] = Empty(self.x, self.y)
        self.x = endX
        self.y = endY
        
    def canMoveList(self, boardList):
        returnCanMoveList = [[]]
        for change in self.changes:
            if (boardList[self.x + change[0]][self.y + change[1]].pieceType == "") or (not self.player == boardList[self.x + change[0]][self.y + change[1]].player):
                returnCanMoveList.append([self.x + change[0], self.y + change[1]])
        return returnCanMoveList

    def canMove(self, endX, endY, canMoveList):
        for move in canMoveList:
            if move == [endX, endY]:
                return True
        return False

    """
    def legalize(self, canMoveList, boardList):

    def isCheck(self, canMoveList, boardList):

    def isCheckMate(self, canMoveList, boardList, tempBoardList):

    """

class Empty(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, [[]], '', False)

class Pawn(Piece):
    def __init__(self, x, y, player):
        if player:
            if y == 1:
                changes = [[0,1], [0,2], [1,1], [-1,1]] #initially can move forward by 1 or 2
            else:
                changes = [[0,1], [1,1], [-1,1]]
            pieceType = 'p'
        else:
            if y == 6:
                changes = [[0,-1], [0,-2], [1,-1], [-1,-1]] #initially can move forward by 1 or 2 (opposite direction)
            else:
                changes = [[0,-1], [1,-1], [-1,-1]]
            pieceType = 'P'
        super().__init__(x, y, changes, pieceType, player)

    def move(self, endX, endY, boardList):
        if len(self.changes) == 4:
            self.changes.pop(1)
        super().move(endX, endY, boardList)

    def canMoveList(self, boardList):
        returnCanMoveList = [[]]
        for change in self.changes:
            if (boardList[self.x + change[0]][self.y + change[1]].pieceType == "" and change[0] == 0) or (not self.player == boardList[self.x + change[0]][self.y + change[1]].player):
                returnCanMoveList.append([self.x + change[0], self.y + change[1]]) #change[0] == 0: unable to move diagonal if not capturing an opponent piece
        return returnCanMoveList

class Rook(Piece):
    def __init__(self, x, y, player):
        changes = [[None for _ in range(2)] for _ in range(28)]
        cnt = 0
        for i in range(1,8):
            changes[4*cnt] = [i,0]
            changes[4*cnt+1] = [-i,0]
            changes[4*cnt+2] = [0,i]
            changes[4*cnt+3] = [0,-i]
            cnt+=1
        if player:
            pieceType = 'r'
        else:
            pieceType = 'R'
        super().__init__(x, y, changes, pieceType, player)

class Knight(Piece):
    def __init__(self, x, y, player):
        changes = [[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]]
        if player:
            pieceType = 'n'
        else:
            pieceType = 'N'        
        super().__init__(x, y, changes, pieceType, player)

class Bishop(Piece):
    def __init__(self, x, y, player):
        changes = [[None for _ in range(2)] for _ in range(28)]
        cnt = 0
        for i in range(1,8):
            changes[4*cnt] = [i,i]
            changes[4*cnt+1] = [i,-i]
            changes[4*cnt+2] = [-i,i]
            changes[4*cnt+3] = [-i,-i]
            cnt+=1
        if player:
            pieceType = 'b'
        else:
            pieceType = 'B'
        super().__init__(x, y, changes, pieceType, player)

class Queen(Piece):
    def __init__(self, x, y, player):
        changes = [[None for _ in range(2)] for _ in range(56)]
        cnt = 0
        for i in range(1,8):
            changes[8*cnt] = [i,0]
            changes[8*cnt+1] = [-i,0]
            changes[8*cnt+2] = [0,i]
            changes[8*cnt+3] = [0,-i]
            changes[8*cnt+4] = [i,i]
            changes[8*cnt+5] = [i,-i]
            changes[8*cnt+6] = [-i,i]
            changes[8*cnt+7] = [-i,-i]
            cnt+=1
        if player:
            pieceType = 'q'
        else:
            pieceType = 'Q'
        super().__init__(x, y, changes, pieceType, player)

class King(Piece):
    def __init__(self, x, y, player):
        changes = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
        if player:
            pieceType = 'k'
        else:
            pieceType = 'K'
        super().__init__(x, y, changes, pieceType, player)