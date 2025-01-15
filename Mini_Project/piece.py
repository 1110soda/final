import pyxel

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
    def __init__(self, x, y, changes, pieceType, player, imageID):
        #index of piece
        self.x = x
        self.y = y
        #list of index changes (movements) of the piece
        self.changes = changes
        #String version of the piece
        self.pieceType = pieceType
        #empty = -1, player = 0, opponent = 1
        self.player = player
        #image file of the piece
        self.imageID = imageID
    
    def toString(self):
        return self.pieceType

    def drawPiece(self, tileSize, boardOffset_x, boardOffset_y):
        playerColor = 1 if self.player == 0 else 0
        if self.imageID >= 0:
            pyxel.blt(self.x * tileSize + boardOffset_x + 32, self.y * tileSize + boardOffset_y + 32, 0, playerColor*16, self.imageID*16, 16, 16, colkey=3, scale=5) #draw each piece to be 5 times its original size (16x16)

    def move(self, endX, endY, boardList): #switch location of the moved piece and the piece/empty at end index
        boardList[endX][endY] = boardList[self.x][self.y]
        boardList[self.x][self.y] = Empty(self.x, self.y)
        self.x = endX
        self.y = endY

    def legalChanges(self, boardList):
        returnLegalChanges = [[None for _ in range(2)] for _ in range(28)]
        CNT = 0
        if self.pieceType.lower() == 'p':
            for change in self.changes:
                if change[0] == 0: #forward movement requirement
                    if 0 <= self.x + change[0] <= 7 and 0 <= self.y + change[1] <= 7:
                        if boardList[self.x + change[0]][self.y + change[1]].pieceType == "":
                            returnLegalChanges[CNT] = change
                            CNT+=1
                else: #diagonal movement requirement
                    if 0 <= self.x + change[0] <= 7 and 0 <= self.y + change[1] <= 7:
                        if not self.player == boardList[self.x + change[0]][self.y + change[1]].player and not boardList[self.x + change[0]][self.y + change[1]].pieceType == "":
                            returnLegalChanges[CNT] = change
                            CNT+=1

        elif self.pieceType.lower() in ['q', 'r', 'b']:
            # Directions for rook, bishop, and queen
            directions = {
                'r': [[1, 0], [-1, 0], [0, 1], [0, -1]],  # Horizontal and vertical
                'b': [[1, 1], [1, -1], [-1, 1], [-1, -1]],  # Diagonal
                'q': [[1, 0], [-1, 0], [0, 1], [0, -1],  # Horizontal, vertical, and diagonal
                    [1, 1], [1, -1], [-1, 1], [-1, -1]]
            }

            # Select the correct direction based on piece type
            pieceDirections = directions[self.pieceType.lower()]

            # Iterate through each direction
            for direction in pieceDirections:
                dx, dy = direction
                x, y = self.x, self.y

                # Move step-by-step in the current direction until hitting edge or piece
                step = 1
                while True:
                    new_x = x + dx * step
                    new_y = y + dy * step

                    # Check if the new position is within the board bounds
                    if not (0 <= new_x < 8 and 0 <= new_y < 8):
                        break  # Stop if the new position is out of bounds
                    
                    # If the square is empty, it's a valid move
                    if boardList[new_x][new_y].pieceType == "":
                        returnLegalChanges[CNT] = [dx * step, dy * step]
                        CNT += 1
                    # If the square contains an opponent's piece, it's a valid capture move
                    elif not self.player == boardList[new_x][new_y].player:
                        returnLegalChanges[CNT] = [dx * step, dy * step]
                        CNT += 1
                        break  # Stop if we encounter an opponent's piece (cannot go further)
                    else:
                        break  # Stop if we encounter our own piece (cannot go further)

                    step += 1  # Move to the next square in this direction

        else:
            for change in self.changes:
                if 0 <= self.x + change[0] <= 7 and 0 <= self.y + change[1] <= 7:
                    if (boardList[self.x + change[0]][self.y + change[1]].pieceType == "") or (not self.player == boardList[self.x + change[0]][self.y + change[1]].player):
                            returnLegalChanges[CNT] = change
                            CNT+=1

        return returnLegalChanges

    def canMove(self, endX, endY, boardList):
        for move in self.canMoveList(self.legalChanges(boardList)):
            if move == [endX, endY]:
                return True
        return False
        
    def canMoveList(self, legalChanges):
        returnCanMoveList = [[None for _ in range(2)] for _ in range(28)]
        CNT = 0
        for legalChange in legalChanges:
            if legalChange[0] == None:
                return returnCanMoveList
            returnCanMoveList[CNT] = [self.x + legalChange[0], self.y + legalChange[1]]
            CNT += 1
        return returnCanMoveList


class Empty(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, [[]], '', -1, -1)

class Pawn(Piece):
    def __init__(self, x, y, player):
        self.moved = False
        if player == 0:
            if not self.moved:
                changes = [[0,-1], [0,-2], [1,-1], [-1,-1]] #initially can move forward by 1 or 2
            else:
                changes = [[0,-1], [1,-1], [-1,-1]]
            pieceType = 'p'
        else:
            if not self.moved:
                changes = [[0,1], [0,2], [1,1], [-1,1]] #initially can move forward by 1 or 2 (opposite direction)
            else:
                changes = [[0,1], [1,1], [-1,1]]
            pieceType = 'P'
        super().__init__(x, y, changes, pieceType, player, 3)

    def move(self, endX, endY, boardList):
        if len(self.changes) == 4:
            self.changes.pop(1)
        super().move(endX, endY, boardList)

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
        if player == 0:
            pieceType = 'r'
        else:
            pieceType = 'R'
        super().__init__(x, y, changes, pieceType, player, 5)

class Knight(Piece):
    def __init__(self, x, y, player):
        changes = [[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]]
        if player == 0:
            pieceType = 'n'
        else:
            pieceType = 'N'        
        super().__init__(x, y, changes, pieceType, player, 2)

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
        if player == 0:
            pieceType = 'b'
        else:
            pieceType = 'B'
        super().__init__(x, y, changes, pieceType, player, 0)

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
        if player == 0:
            pieceType = 'q'
        else:
            pieceType = 'Q'
        super().__init__(x, y, changes, pieceType, player, 4)

class King(Piece):
    def __init__(self, x, y, player):
        changes = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
        if player == 0:
            pieceType = 'k'
        else:
            pieceType = 'K'
        super().__init__(x, y, changes, pieceType, player, 1)