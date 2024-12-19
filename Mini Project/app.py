import pyxel
from piece import Piece
from board import Board

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title = "Chess", fps = 30, display_scale = 12, capture_scale = 6)
        gameBoard = Board()
        self.boardToString(gameBoard)
        tempBoard = gameBoard #used in isCheckMate() to simulate board after one move
        
        #Boolean for selecting the screen to be displayed
        START = True
        PLAYERSELECT = MODESELECT = DETAILSELECT = CHESSBOARD = GAMEOVER = False
        pyxel.run(self.update, self.draw)

    def boardToString(self, gameBoard):
        gameBoardStr = gameBoard.getBoardStr()
        for j in range(len(gameBoardStr[0])):
            for i in range(len(gameBoardStr)):
                print(gameBoardStr[i][j], end=" ")
            print()

    def update(self):
        if START:
        
        elif PLAYERSELECT:

        elif MODESELECT:

        elif DETAILSELECT:

        elif CHESSBOARD:

        elif GAMEOVER:

        else:
            print("Screen change error, boolean all set to False")
            pyxel.quit()
    
    def draw(self):
        if START:
        
        elif PLAYERSELECT:

        elif MODESELECT:

        elif DETAILSELECT:

        elif CHESSBOARD:

        elif GAMEOVER:
            pyxel.cls(col = 9)
            displayText = ["GAMEOVER", "Q (Quit)", "R (Restart)"][:]


App()