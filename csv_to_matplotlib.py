import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

COLUMNS = ['X', 'Y']
ANOTATED = []
ANOTATED_LIST = []
xLabel = "x label here"
yLabel = "y label here"
title = "title here"

xData = []
yData = []


class QtLab(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("csv_to_matplotlib.ui", self)
        self.setWindowTitle("CSV to graph")
        self.loadCSV.clicked.connect(self.loadCSVF)
        self.anotate.clicked.connect(self.anotateF)
        self.listX.itemDoubleClicked.connect(self.listXF)
        self.titleGraph.returnPressed.connect(self.titleGraphF)
        self.xlabelGraph.returnPressed.connect(self.xlabelGraphF)
        self.ylabelGraph.returnPressed.connect(self.ylabelGraphF)

        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

        self.listX.addItem("TEST")
        self.titleGraph.setText(title)
        self.xlabelGraph.setText(xLabel)
        self.ylabelGraph.setText(yLabel)

    def titleGraphF(self):
        global title
        title = self.titleGraph.text()

    def xlabelGraphF(self):
        global xLabel
        xLabel = self.xlabelGraph.text()

    def ylabelGraphF(self):
        global yLabel
        yLabel = self.ylabelGraph.text()

    def loadCSVF(self):
        global ANOTATED,ANOTATED_LIST, xData, yData, xLabel, yLabel, title
        ANOTATED = []
        ANOTATED_LIST = []
        path = QFileDialog.getOpenFileName(self, 'Open a file')
        data = pd.read_csv(path[0], skiprows=1, names=['X', 'Y'])

        xData = [data.X[i] for i in range(len(data.X))]
        yData = [data.Y[i] for i in range(len(data.Y))]

        strX = [str(data.X[i]) for i in range(len(data.X))]

        self.listX.clear()
        self.listX.addItems(strX)

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(data.X, data.Y)
        self.MplWidget.canvas.axes.set_title(title)
        self.MplWidget.canvas.axes.set_xlabel(xLabel)
        self.MplWidget.canvas.axes.set_ylabel(yLabel)
        self.MplWidget.canvas.draw()

    def anotateF(self):
        global ANOTATED_LIST, ANOTATED
        for x in ANOTATED_LIST:
            x.remove()
        ANOTATED = []
        ANOTATED_LIST = []

    def listXF(self, item):
        global ANOTATED, ANOTATED_LIST, xData, yData
        clicked = int(item.text())
        if clicked in ANOTATED:
            print(ANOTATED)
            n = ANOTATED.index(clicked)
            ANOTATED_LIST[n].remove()
            ANOTATED.pop(n)
            ANOTATED_LIST.pop(n)
        else:
            ANOTATED.append(clicked)
            n = xData.index(clicked)
            labelxy = (clicked, yData[n])
            ann = self.MplWidget.canvas.axes.annotate("({}, {})".format(clicked, yData[n]),
                                                      xy=labelxy,
                                                      xycoords='data',
                                                      xytext=(self.MplWidget.get_X(),self.MplWidget.get_Y()),
                                                      textcoords='data',
                                                      size=10,
                                                      va="center",
                                                      ha="center",
                                                      color="red",
                                                      fontsize=10,
                                                      arrowprops=dict(arrowstyle="->",
                                                                      connectionstyle="arc3"),
                                                      )
            ANOTATED_LIST.append(ann)

        self.MplWidget.canvas.draw()


if __name__ == "__main__":
    app = QApplication([])
    windows = QtLab()
    windows.show()
    app.exec_()


