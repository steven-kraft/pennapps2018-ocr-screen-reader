from PIL import Image
from PIL import ImageGrab
import pytesseract
import cv2
import os
from gtts import gTTS
from playsound import playsound
from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import tkinter as tk
import numpy as np

def tts(msg):
    file = "message.mp3"
    gTTS(text=msg, lang='en').save(file)
    playsound(file)
    os.remove(file)

def readImage(image):
    text = pytesseract.image_to_string(Image.open(image))
    os.remove(image)
    print(text)
    tts(text)

class Snipper(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        self.setGeometry(0, 0, root.winfo_screenwidth(), root.winfo_screenheight())
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img.save('image.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        readImage("image.png")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Snipper()
    window.show()
    sys.exit(app.exec_())
