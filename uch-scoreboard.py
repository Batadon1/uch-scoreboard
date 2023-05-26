# vesion: 1.0
# date: 05/26/2023
# author: Batadon/Leon

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# --------------------------------------------------------------------------------------------------- #

P1 = "Player1"
P2 = "Player2"
POINTS_TO_WIN = 2
ROUND_LIMIT = 10
FONT = "Roboto"

# --------------------------------------------------------------------------------------------------- #

WHITE = "#ECEFF1"
GREY = "#455A64"
BLACK = "#263238"
GREEN = "#2E7D32"

def formatText(label, pos, text, color, fontSize):
    qFont = QFont()
    qFont.setFamily(FONT)
    qFont.setPointSize(16)

    label.move(pos[0]+11, pos[1]+6)
    label.setText(text)
    label.setFont(qFont)
    label.setStyleSheet("color: " + color + "; font-size: " + str(fontSize) + "px; font-weight: bold;")

class Window(QWidget):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(800, 200)
        self.setWindowTitle("UCH Scoreboard")

        self.gameNr = 1
        self.roundNr = 1
        self.p1SetScore = 0
        self.p2SetScore = 0
        self.p1GameScore = 0
        self.p2GameScore = 0

        # Row 1
        self.textHead = QLabel(self)
        self.headGamemode = "First to " + str(POINTS_TO_WIN)
        self.headGameNr = "Game " + str(self.gameNr)
        self.headRoundNr = "Round " + str(self.roundNr) + "/" + str(ROUND_LIMIT)
        self.updateHead()
        self.textSet = QLabel(self)
        formatText(self.textSet, [530, 0], "Set", WHITE, 40)
        self.textGame = QLabel(self)
        formatText(self.textGame, [640, 0], "Game", WHITE, 40)
        # Row 2
        self.p1Name = QLabel(self)
        formatText(self.p1Name, [0, 65], P1, BLACK, 40)
        self.textP1Set = QLabel(self)
        formatText(self.textP1Set, [550, 65], str(self.p1SetScore), WHITE, 40)
        self.textP1Game = QLabel(self)
        formatText(self.textP1Game, [685, 65], str(self.p2SetScore), WHITE, 40)
        # Row 3
        self.p2Name = QLabel(self)
        formatText(self.p2Name, [0, 135], P2, BLACK, 40)
        self.textP2Set = QLabel(self)
        formatText(self.textP2Set, [550, 135], str(self.p1GameScore), WHITE, 40)
        self.textP2Game = QLabel(self)
        formatText(self.textP2Game, [685, 135], str(self.p2GameScore), WHITE, 40)

        endGameButton = QPushButton("", self)
        endGameButton.resize(500, 60)
        endGameButton.move(0, 0)
        endGameButton.clicked.connect(self.endGame)
        endGameButton.setFlat(True)

        p1Button = QPushButton("", self)
        p1Button.resize(500, 70)
        p1Button.move(0, 60)
        p1Button.clicked.connect(self.p1Scored)
        p1Button.setFlat(True)

        p2Button = QPushButton("", self)
        p2Button.resize(500, 70)
        p2Button.move(0, 130)
        p2Button.clicked.connect(self.p2Scored)
        p2Button.setFlat(True)

        noScoreButton = QPushButton("", self)
        noScoreButton.resize(300, 140)
        noScoreButton.move(500, 60)
        noScoreButton.clicked.connect(self.noScore)
        noScoreButton.setFlat(True)

    def updateHead(self):
        headText = self.headGamemode + "  -  " + self.headGameNr
        if self.headRoundNr != "":
            headText += "  -  " + self.headRoundNr + "  "
        formatText(self.textHead, [0, 15], headText, WHITE, 25)

    def endGame(self):
        # Update scores
        if self.p1GameScore > self.p2GameScore:
            self.p1SetScore += 1
        else:
            self.p2SetScore += 1
        self.p1GameScore = 0
        self.p2GameScore = 0
        
        # Update rounds
        self.gameNr += 1
        self.roundNr = 1

        self.updateScoreboard()

    def p1Scored(self):
        self.p1GameScore += 1
        self.roundNr += 1
        self.textP1Game.setText(str(self.p1GameScore))
        self.updateScoreboard()

    def p2Scored(self):
        self.p2GameScore += 1
        self.roundNr += 1
        self.textP2Game.setText(str(self.p2GameScore))
        self.updateScoreboard()

    def noScore(self):
        self.roundNr += 1
        self.updateScoreboard()

    def updateScoreboard(self):
        # Show scores
        self.textP1Game.setText(str(self.p1GameScore))
        self.textP1Set.setText(str(self.p1SetScore))
        self.textP2Game.setText(str(self.p2GameScore))
        self.textP2Set.setText(str(self.p2SetScore))
        self.headGameNr = "Game " + str(self.gameNr)
        overtime = (self.roundNr > ROUND_LIMIT) and (self.p1GameScore == self.p2GameScore)
        result = ((self.roundNr > ROUND_LIMIT) and (self.p1GameScore != self.p2GameScore)) or (self.roundNr > ROUND_LIMIT + 1)
        if overtime:
            self.headRoundNr = "Overtime"
        elif result:
            self.headRoundNr = ""
        else:
            self.headRoundNr = "Round " + str(self.roundNr) + "/" + str(ROUND_LIMIT)
        
        if max(self.p1SetScore, self.p2SetScore) >= POINTS_TO_WIN:
            self.headGameNr = "Results"
            self.headRoundNr = ""
        self.updateHead()

        self.update()

    def paintEvent(self, event):
        bg = QPainter(self)
        bg.fillRect(0, 0, 800, 60, QColor(GREY))
        bg.fillRect(0, 60, 500, 140, QColor(WHITE))
        bg.fillRect(500, 60, 300, 140, QColor(GREEN))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
   
if __name__ == '__main__':
   app = QApplication(sys.argv)
   w = Window()
   w.show()
   sys.exit(app.exec_())