import sys
import numpy as np
from PyQt4 import QtGui
import cursortest
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.widgets import Cursor

class guiapp(QtGui.QMainWindow, cursortest.Ui_Dialog):
    def __init__(self):
        super(self.__class__, self).__init__()

        self.setupUi(self)

        self.setupfigure()

        self.populateplt()

        self.addcursor()

        self.visible = True
        self.horizOn = True
        self.vertOn = True
        self.useblit = True
        self.background = None
        self.needclear = False

        self.canvas.setVisible(True)
        cid2 = self.canvas.mpl_connect('motion_notify_event', self.onmove)

    def setupfigure(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.plt2d)
        self.ax.set_title('title')
        self.ax.set_xlabel('x label')
        self.ax.set_ylabel('y label')

        # navigation toolbar
        self.navbar = NavigationToolbar(self.canvas, self.plt2d, coordinates=True)

    def populateplt(self):
        data = np.random.rand(200,200)
        self.ax.imshow(data)

    def addcursor(self):
        self.cursor = Cursor(self.ax,horizOn=True,vertOn=True,useblit=False, color='black')

        self.lineh = self.ax.axhline(self.ax.get_ybound()[0], visible=False)
        self.linev = self.ax.axvline(self.ax.get_xbound()[0], visible=False)

    def onmove(self, event):
        'on mouse motion draw the cursor if visible'
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible: return
        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()


    def _update(self):

        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.canvas.blit(self.ax.bbox)
        else:
            self.canvas.draw_idle()

        return False


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = guiapp()
    form.show()
    app.exec_()
