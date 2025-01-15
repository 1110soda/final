import pyxel, os, random
from piece import Piece
from board import Board

screenWidth, screenHeight = 1000, 800
tileSize = 80 #5 times the original piece image size(16x16)
#center the chess board
boardOffset_x = (screenWidth - tileSize*8)//2
boardOffset_y = (screenHeight - tileSize*8)//2

class App:
    def __init__(self):
        pyxel.init(screenWidth, screenHeight, title = "Chess", fps = 30, display_scale = 12, capture_scale = 6)

        pyxel.mouse(True)

        self.board = Board()
        self.gameBoard = self.board.getBoard()
        self.boardToString()

        pyxel.load("chessPiece/chessPiece.pyxres")

        self.umplus12 = pyxel.Font("umplus_j12r.bdf") #custom font

        #Boolean for selecting the screen to be displayed
        self.START = True
        self.PLAYERSELECT = self.ENTERNAME = self.ENTERNAME2 = self.MODESELECT = self.CHESSBOARD = self.GAMEOVER = False
        self.playerName, self.opponentName, self.winnerName = "", "", ""
        self.mode = ""
        self.name_INPUT = ""

        self.currentPlayer = 0 #player = 0, opponent = 1
        self.selectedPiece = None
        self.selected = self.moved = False
        self.cursor_x, self.cursor_y = 0, 0 #converted to the index of the piece (0-7)
        self.firstClick = False

        self.popUpMessage = None
        self.popUpTimer = 0

        pyxel.run(self.update, self.draw)

    def resetGame(self):
        self.board = Board()
        self.gameBoard = self.board.getBoard()
        self.boardToString()

        self.CHESSBOARD = True
        self.GAMEOVER = False

        self.currentPlayer = 0 #player = 0, opponent = 1
        self.selectedPiece = None
        self.selected = self.moved = False
        self.cursor_x, self.cursor_y = 0, 0 #converted to the index of the piece (0-7)
        self.firstClick = False

    def drawText(self, x, y, text, color=7, bcolor=5):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx != 0 or dy != 0:
                    pyxel.text(x + dx, y + dy, text, bcolor, self.umplus12)
        pyxel.text(x, y, text, color, self.umplus12)

    def drawPopUp(self, text):
        if self.popUpTimer > 0:
            self.popUpTimer -= 1
        else:
            return False
        
        textWidth = len(text)*6
        textHeight = 8
        center_x = (screenWidth - textWidth) // 2
        center_y = (screenHeight - textHeight) // 2

        pyxel.rectb(center_x - 7, center_y - 7, textWidth + 14, textHeight + 14, 8)  # Red border
        pyxel.rect(center_x - 6, center_y - 6, textWidth + 12, textHeight + 12, 0)   # Black background
        self.drawText(center_x, center_y, text)

        return True

    def drawBoard(self):
        for row in range(8):
            for col in range(8):
                color = 7 if (row+col)%2 == 0 else 6 #alternate color
                pyxel.rect(col*tileSize+boardOffset_x, row*tileSize+boardOffset_y, tileSize, tileSize, color)

    def drawPieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.gameBoard[row][col]
                piece.drawPiece(tileSize, boardOffset_x, boardOffset_y)
    
    def drawHighlight(self):
        if self.selectedPiece:
            # Highlight selected piece in orange
            for i in range(5):
                pyxel.rectb(self.selectedPiece.x * tileSize + boardOffset_x + i,
                        self.selectedPiece.y * tileSize + boardOffset_y + i,
                        tileSize - 2*i, tileSize - 2*i, pyxel.COLOR_ORANGE)

            # Highlight legal moves in yellow
            for move in self.selectedPiece.canMoveList(self.selectedPiece.legalChanges(self.gameBoard)):
                if move[0] == None:
                    return
                for i in range(5):
                    pyxel.rectb(move[0] * tileSize + boardOffset_x + i,
                            move[1] * tileSize + boardOffset_y + i,
                            tileSize - 2*i, tileSize - 2*i, pyxel.COLOR_YELLOW)

    def selectPiece(self, mouse_x, mouse_y):
        print(mouse_x, mouse_y)
        if mouse_x < 0 or mouse_x > 7 or mouse_y < 0 or mouse_y > 7:
            return
        self.selectedPiece = self.gameBoard[mouse_x][mouse_y]
        print(self.selectedPiece.toString(), self.selectedPiece.player, self.currentPlayer)
        if self.selectedPiece.player == self.currentPlayer:
            self.selected = True
        else:
            self.selectedPiece = None

    def boardToString(self):
        gameBoardStr = self.board.getBoardStr()
        for j in range(len(gameBoardStr[0])):
            for i in range(len(gameBoardStr)):
                print(gameBoardStr[i][j], end=" ")
            print()

    def isGameOver(self, player):
        for x in range(8):
            for y in range(8):
                if self.gameBoard[x][y].player == player and self.gameBoard[x][y].pieceType.lower() == 'k':
                    return False
        return True
    
    def isInCheck(self, player):
        kingX, kingY = 0, 0
        for x in range(8):
            for y in range(8):
                if self.gameBoard[x][y].player == player and self.gameBoard[x][y].pieceType.lower() == 'k':
                    kingX, kingY = x, y
        for x in range(8):
            for y in range(8):
                if (self.gameBoard[x][y].player != player) and (self.gameBoard[x][y].player != -1): #select all opponent pieces
                    if self.gameBoard[x][y].canMove(kingX, kingY, self.gameBoard):
                        return True
        return False

    def randomMove(self):
        # Collect all pieces for the CPU (player 1)
        cpuPieces = []
        for x in range(8):
            for y in range(8):
                piece = self.gameBoard[x][y]
                if piece.player == 1:  # CPU pieces
                    cpuPieces.append(piece)

        if len(cpuPieces) == 0:
            return False  # No pieces left to move

        # Select a random piece from the CPU pieces
        piece = random.choice(cpuPieces)
        print(f"CPU selected piece: {piece.pieceType} at ({piece.x}, {piece.y})")

        # Get all legal moves for that piece
        legalMoves = []
        for move in piece.canMoveList(piece.legalChanges(self.gameBoard)):
            if move[0] == None:
                break
            legalMoves.append(move)

        if len(legalMoves) == 0:
            return False #No legal moves for that piece

        move = random.choice(legalMoves)

        print(f"CPU selected move: ({move[0]}, {move[1]})")

        # Make the move if valid
        if piece.canMove(move[0], move[1], self.gameBoard):
            piece.move(move[0], move[1], self.gameBoard)
            return True  # Move was made
        return False  # No valid move found

    def update(self):
        if self.START:
            if pyxel.btnp(pyxel.KEY_RETURN):  # Start the game
                self.START = False
                self.PLAYERSELECT = True
        elif self.PLAYERSELECT:
            # Handle text input for player name
            if pyxel.btnp(pyxel.KEY_1):  # Select one player (single player)
                self.PLAYERSELECT = False
                self.ENTERNAME = True
                self.mode = "single"  # Set to single-player mode
            elif pyxel.btnp(pyxel.KEY_2):  # Select multiplayer
                self.PLAYERSELECT = False
                self.ENTERNAME = True
                self.mode = "multiplayer"  # Set to multiplayer mode
        elif self.ENTERNAME:
            # Handle name input
            if pyxel.btnp(pyxel.KEY_RETURN):  # Submit name input and proceed to game
                if self.mode == "single":
                    self.playerName = self.name_INPUT
                    self.opponentName = "CPU"
                    self.ENTERNAME = False
                    self.CHESSBOARD = True
                elif self.mode == "multiplayer":
                    self.playerName = self.name_INPUT
                    self.name_INPUT = ""
                    self.ENTERNAME = False
                    self.ENTERNAME2 = True
            else:
                if pyxel.btnp(pyxel.KEY_BACKSPACE):  # Delete last character
                    self.name_INPUT = self.name_INPUT[:-1]
                else:
                    # Add character to input string (limit to a certain length)
                    for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                        if pyxel.btnp(key):
                            self.name_INPUT += chr(key)
                    for num in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
                        if pyxel.btnp(num):
                            self.name_INPUT += chr(num-pyxel.KEY_0 + ord('0'))
        elif self.ENTERNAME2:
            # Handle name input
            if pyxel.btnp(pyxel.KEY_RETURN):  # Submit name input and proceed to game
                self.opponentName = self.name_INPUT    
                self.ENTERNAME2 = False
                self.CHESSBOARD = True
            else:
                if pyxel.btnp(pyxel.KEY_BACKSPACE):  # Delete last character
                    self.name_INPUT = self.name_INPUT[:-1]
                else:
                    # Add character to input string (limit to a certain length)
                    for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
                        if pyxel.btnp(key):
                            self.name_INPUT += chr(key)
                    for num in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
                        if pyxel.btnp(num):
                            self.name_INPUT += chr(num-pyxel.KEY_0 + ord('0'))

###################################################################################################                            
        elif self.CHESSBOARD:
            # Mouse cursor position
            self.cursor_x = (pyxel.mouse_x - boardOffset_x) // tileSize
            self.cursor_y = (pyxel.mouse_y - boardOffset_y) // tileSize

            # Handle left-click for piece selection
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and not self.selected:  # Left mouse button click
                self.selectPiece(self.cursor_x, self.cursor_y)
                self.firstClick = True

            # Handle piece movement (left-click again to move the piece)
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.selected and not self.firstClick:
                if self.cursor_x == self.selectedPiece.x and self.cursor_y == self.selectedPiece.y:
                    print("cancelled")
                    self.selected = False
                    self.selectedPiece = None
                elif self.cursor_x >= 0 and self.cursor_x <= 7 and self.cursor_y >= 0 and self.cursor_y <= 7:        
                    if self.selectedPiece.canMove(self.cursor_x, self.cursor_y, self.gameBoard):
                        self.selectedPiece.move(self.cursor_x, self.cursor_y, self.gameBoard) # Left mouse button click to move
                        self.selected = False
                        self.selectedPiece = None
                        self.moved = True

            #CPU's turn (self.mode == "single")
            if self.mode == "single" and self.currentPlayer == 1:
                print("CPU's turn")
                if self.randomMove():  # CPU makes a random move
                    self.moved = True

            if self.firstClick:
                self.firstClick = not self.firstClick

            if self.moved:
                if self.currentPlayer == 0:
                    self.popUpMessage = f"{self.opponentName}'s turn"
                    self.currentPlayer = 1
                else:
                    self.popUpMessage = f"{self.playerName}'s turn"
                    self.currentPlayer = 0
                self.popUpTimer = 60
                self.moved = False
            elif self.isInCheck(0) and self.popUpTimer == 0:
                if self.isInCheck(1):
                    self.popUpMessage = "Both players are in check"
                else:
                    self.popUpMessage = f"{self.playerName} in check"
                self.popUpTimer = 60
            elif self.isInCheck(1) and self.popUpTimer == 0:
                self.popUpMessage = f"{self.opponentName} in check"
                self.popUpTimer = 60
    
            if self.isGameOver(self.currentPlayer):
                self.winnerName = self.playerName if self.currentPlayer == 1 else self.opponentName
                self.CHESSBOARD = False
                self.GAMEOVER = True

###################################################################################################

        elif self.GAMEOVER:
            if pyxel.btnp(pyxel.KEY_Q):
                pyxel.quit()  # Quit the game
            if pyxel.btnp(pyxel.KEY_R):
                self.resetGame()
    
    def draw(self):
        if self.START:
            pyxel.cls(0)
            self.drawText(50, 50, "CHESS")
            self.drawText(50, 70, "PRESS ENTER TO START")
        elif self.PLAYERSELECT:
            pyxel.cls(0)
            self.drawText(50, 50, "Select Player Mode")
            self.drawText(50, 70, "Press 1 for Single Player")
            self.drawText(50, 90, "Press 2 for Multiplayer")
        elif self.ENTERNAME:
            pyxel.cls(0)
            self.drawText(50, 50, "Enter Your Name")
            self.drawText(50, 70, "Player Name: " + self.name_INPUT)
            if self.mode == "single":
                self.drawText(50, 90, "Press Enter to Confirm")
            elif self.mode == "multiplayer":
                self.drawText(50, 90, "Press Enter to Confirm & Proceed to the Name of the Opponent Player")
        elif self.ENTERNAME2:
            pyxel.cls(0)
            self.drawText(50, 50, "Enter Your (Opponent) Name")
            self.drawText(50, 70, "Opponent Name: " + self.name_INPUT)
        elif self.CHESSBOARD:
            pyxel.cls(0)
            self.drawText(50, 50, "Player: " + self.playerName)
            self.drawText(50, 70, "Opponent: " + self.opponentName)
            self.drawBoard()
            self.drawPieces()
            #Highlight movable areas after selection
            if self.selected:
                self.drawHighlight()
            #Draw popup messages on top of all other items
            if self.popUpMessage and self.popUpTimer > 0:
                self.drawPopUp(self.popUpMessage)
        elif self.GAMEOVER:
            pyxel.cls(0)
            self.drawText(50, 50, "WINNER: " + self.winnerName)
            self.drawText(50, 70, "Press Q to Quit or R to Restart")

App()