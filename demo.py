import os
import sys
import random
from enum import IntEnum
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt


# Enumerate the directions
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Puzzle(QWidget):

    def __init__(self):

        super().__init__()

        self.PUZZLE_HEIGHT = 2
        self.PUZZLE_WIDTH = 4
        self.blocks = []

        self.labels = None
        self.space_row = None
        self.space_col = None
        self.randomLabels()

        self.grid = QGridLayout()
        # set the space between blocks
        self.grid.setSpacing(10)

        self.initUI()

    def randomLabels(self):
        while True:
            self.labels = random.sample(list(range(0, self.PUZZLE_HEIGHT * self.PUZZLE_WIDTH)),
                                        self.PUZZLE_HEIGHT * self.PUZZLE_WIDTH)
            for i in range(self.PUZZLE_HEIGHT):
                for j in range(self.PUZZLE_WIDTH):
                    if self.labels[i * self.PUZZLE_WIDTH + j] == 0:
                        self.space_row = i
                        self.space_col = j
                        break
            if self.isSolvable():
                break

    def calculateInversion(self):
        count = 0
        for i in range(len(self.labels)):
            if self.labels[i] == 0:
                continue
            for j in range(i):
                if self.labels[j] == 0:
                    continue
                if self.labels[i] < self.labels[j]:
                    count += 1
        return count

    def isSolvable(self):
        if self.PUZZLE_WIDTH % 2 == 1:
            if self.calculateInversion() % 2 == 0:
                return True
            return False
        else:
            spaceRowIndexBackward = self.PUZZLE_HEIGHT - self.space_row
            numInversion = self.calculateInversion()

            if (spaceRowIndexBackward + numInversion) % 2 == 1:
                return True
            return False

    def initUI(self):

        self.setLayout(self.grid)
        # set the window's height and width
        self.setFixedSize(100 * self.PUZZLE_WIDTH, 100 * self.PUZZLE_HEIGHT)
        # set the title
        self.setWindowTitle('Demo')
        # set the background color
        self.setStyleSheet("background-color:white;")
        self.blocksInit()
        self.show()

    def blocksInit(self):

        for row in range(self.PUZZLE_HEIGHT):
            self.blocks.append([])
            self.blocks[row] = [x for x in self.labels[row * self.PUZZLE_WIDTH:(row + 1) * self.PUZZLE_WIDTH]]

        self.updatePanel()

    def keyPressEvent(self, event):
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)

        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, 'Congratulation', 'Congratulation!'):
                # restart
                self.blocksInit()

    def move(self, direction):
        if (direction == Direction.UP):
            if self.space_row != self.PUZZLE_HEIGHT - 1:
                self.blocks[self.space_row][self.space_col] = self.blocks[self.space_row + 1][self.space_col]
                self.blocks[self.space_row + 1][self.space_col] = 0
                self.space_row += 1
        if (direction == Direction.DOWN):
            if self.space_row != 0:
                self.blocks[self.space_row][self.space_col] = self.blocks[self.space_row - 1][self.space_col]
                self.blocks[self.space_row - 1][self.space_col] = 0
                self.space_row -= 1
        if (direction == Direction.LEFT):
            if self.space_col != self.PUZZLE_WIDTH - 1:
                self.blocks[self.space_row][self.space_col] = self.blocks[self.space_row][self.space_col + 1]
                self.blocks[self.space_row][self.space_col + 1] = 0
                self.space_col += 1
        if (direction == Direction.RIGHT):
            if self.space_col != 0:
                self.blocks[self.space_row][self.space_col] = self.blocks[self.space_row][self.space_col - 1]
                self.blocks[self.space_row][self.space_col - 1] = 0
                self.space_col -= 1

    def updatePanel(self):
        for row in range(self.PUZZLE_HEIGHT):
            for col in range(self.PUZZLE_WIDTH):
                self.grid.addWidget(Block(self.blocks[row][col]), row, col)

        self.setLayout(self.grid)

    def checkResult(self):

        if self.blocks[self.PUZZLE_HEIGHT - 1][self.PUZZLE_WIDTH - 1] != 0:
            return False

        for row in range(self.PUZZLE_HEIGHT):
            for col in range(self.PUZZLE_WIDTH):
                if row == self.PUZZLE_HEIGHT - 1 and col == self.PUZZLE_WIDTH - 1:
                    pass
                elif self.blocks[row][col] != row * self.PUZZLE_WIDTH + col + 1:
                    return False
        return True


class Block(QLabel):

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(80, 80)

        # set the font
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # set the font style
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.blue)
        self.setPalette(pa)

        # set the label position
        self.setAlignment(Qt.AlignCenter)

        # set the background image
        if self.number == 0:
            self.setStyleSheet("background-color:white; border-radius:5px;")
        else:
            pwd = os.path.abspath('.')
            url = os.path.join(pwd, 'images', "f-{}.png".format(number - 1))
            # for Windows System
            url = url.replace("\\", "/")
            self.setStyleSheet("border-image:url('%s'); border-radius:5px;" % url)
            self.setText(str(self.number))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Puzzle()
    sys.exit(app.exec_())
