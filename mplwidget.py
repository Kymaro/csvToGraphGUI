# ------------------------------------------------------
# -------------------- mplwidget.py --------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from matplotlib.figure import Figure


Xmpl = 0
Ympl = 0

class MplWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.canvas = FigureCanvasQTAgg(Figure())

        self.X = 0
        self.Y = 0

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)

        self.canvas.mpl_connect("button_press_event", self.on_press)

    def on_press(self, event):
        global Xmpl,Ympl
        print("press")
        print("event.xdata", event.xdata)
        print("event.ydata", event.ydata)
        Xmpl = event.xdata
        Ympl = event.ydata

    def get_X(self):
        return Xmpl
    def get_Y(self):
        return Ympl