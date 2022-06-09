from PyQt5.QtWidgets import *

class Login(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(300, 200)
        self.setWindowTitle('Log in')

        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(self.password.Password)
        self.connect_button = QPushButton('Connect', enabled=False)

        layout = QGridLayout(self)
        layout.addWidget(QLabel('Username:'), 0, 0)
        layout.addWidget(self.username, 0, 1)
        layout.addWidget(QLabel('Password:'), 1, 0)
        layout.addWidget(self.password, 1, 1)
        layout.addWidget(self.connect_button, 2, 0, 1, 2)

        self.connect_button.clicked.connect(self.handleConnexion)
        self.username.textChanged.connect(self.checkFields)
        self.password.textChanged.connect(self.checkFields)

    def checkFields(self):
        if self.username.text() and self.password.text():
            self.connect_button.setEnabled(True)
        else:
            self.connect_button.setEnabled(False)

    def handleConnexion(self):
        if self.username.text() == 'admin' and self.password.text() == '1':
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 
                'Invalid username or password!')