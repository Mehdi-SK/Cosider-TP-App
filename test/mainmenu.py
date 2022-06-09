from PyQt5.QtWidgets import *
from login import Login

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(300, 200)
        self.setWindowTitle('Main menu')

        disconnect_button = QPushButton('Disconnect')
        self.setCentralWidget(disconnect_button)

        # only for a *persistent* login dialog (*see below)
        self.login = Login()

        disconnect_button.clicked.connect(self.disconnect)

    def start(self):
        # put here some function that might check for a 'previous' logged in
        # state, possibly stored using QSettings.
        # in this case, we just assume that the user has never previously
        # logged in, so we automatically show the login window; if the above
        # function returns True instead, we can safely show the main window
        logged = False

        if logged:
            self.show()
        else:
            self.showLogin()

    def disconnect(self):
        self.hide()
        self.showLogin()

    def showLogin(self):
        if self.login.exec():
            self.show()

        # alternatively (*see below):
        # login = Login()
        # if login.exec():
        #     self.show()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.start()
    sys.exit(app.exec())