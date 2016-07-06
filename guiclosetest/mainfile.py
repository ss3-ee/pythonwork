import sys
import guiclosetest as gct
from PyQt4 import QtGui
import pickle
# import gui_utils as gu

# testing close window event

class guiapp(QtGui.QMainWindow, gct.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.onclick)

    def onclick(self):
        print('btn clicked' )
        self.printlinein()

    def closeEvent(self, *args, **kwargs):
        print('closing')

    def printlinein(self):
        data = {}
        for attr in dir(self):
            if 'lineEdit' in attr:
                data[attr] = getattr(self,attr).text()

        pickle.dump(data, open('datadump.p','wb'))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form =  guiapp()
    form.show()
    app.exec_()