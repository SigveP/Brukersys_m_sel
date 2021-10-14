# python 3.9.6 64-bit

import sql_functions as sqlf
import PyQt6.QtWidgets as QtW
import PyQt6.QtGui as QtG
from sys import argv
from datetime import datetime


class MainWindow(QtW.QWidget):
    def __init__(self, user):
        super().__init__()

        self.user = user  # brukernavn
        self.last_check = datetime.now()  # hvis under 3 min: ikke spør om passord
        self.images = {
            'seal': (  # bilde, beskrivelse
                QtG.QPixmap('images/sel.jpg').scaledToWidth(200),
                "en klump med fet og dyn."
            )
        }

        contentlayout = QtW.QVBoxLayout()
        content_image = QtW.QLabel()
        content_image.setPixmap(self.images['seal'][0])
        content_label = QtW.QLabel(
            text="Bilde av {}".format(self.images['seal'][1]))
        contentlayout.addWidget(content_image)
        contentlayout.addWidget(content_label)

        buttonlayout = QtW.QHBoxLayout()
        logout_button = QtW.QPushButton(text="Logout")
        logout_button.clicked.connect(self.logout)
        buttonlayout.addWidget(logout_button)

        windowlayout = QtW.QVBoxLayout()
        windowlayout.addLayout(contentlayout)
        windowlayout.addLayout(buttonlayout)

        self.setLayout(windowlayout)
        self.show()

    def check(self):
        time = datetime.now()

        if (time - self.last_check).min < 3:
            return True
        else:
            access = self.getpassword()
            if access:
                self.last_check = time
            return access

    def getpassword(self):
        windows['passwordcheck'] = LoginWindow(
            getpassword=True, user=self.user)

    def logout(self):
        self.destroy()
        windows['login'].show()

    def closeEvent(self, a0: QtG.QCloseEvent) -> None:
        exit_program()


class CreateUserWindow(QtW.QWidget):
    def __init__(self):
        super().__init__()

        namelayout = QtW.QHBoxLayout()
        name_label = QtW.QLabel(text="Username: ")
        name_field = QtW.QLineEdit()
        namelayout.addWidget(name_label)
        namelayout.addWidget(name_field)

        passwordlayout = QtW.QHBoxLayout()
        password_label = QtW.QLabel(text=" Password: ")
        password_field = QtW.QLineEdit()
        password_field.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        passwordlayout.addWidget(password_label)
        passwordlayout.addWidget(password_field)

        rpasswordlayout = QtW.QHBoxLayout()
        rpassword_label = QtW.QLabel(text=" Password: ")
        rpassword_field = QtW.QLineEdit()
        rpassword_field.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        rpasswordlayout.addWidget(rpassword_label)
        rpasswordlayout.addWidget(rpassword_field)

        create_button = QtW.QPushButton(text="Create Account")
        create_button.clicked.connect(lambda: self.createuser(
            name_field.text(),
            password_field.text(),
            rpassword_field.text()
        ))

        windowlayout = QtW.QVBoxLayout()
        windowlayout.addLayout(namelayout)
        windowlayout.addLayout(passwordlayout)
        windowlayout.addLayout(rpasswordlayout)
        windowlayout.addWidget(create_button)

        self.setLayout(windowlayout)
        self.show()

    def createuser(self, username, password, rpassword):
        if password != rpassword:
            return
        try:
            sqlf.add_user(username, password)
            self.destroy()
        except:
            return


class LoginWindow(QtW.QWidget):
    def __init__(self, **kwargs):
        super().__init__()

        try:
            print('getpassword: {0}'.format(kwargs['getpassword']))
        except:
            print('getpassword: False')
            kwargs['getpassword'] = False

        self.kwargs = kwargs  # for funksjonene

        namelayout = QtW.QHBoxLayout()
        name_label = QtW.QLabel(text="Username: ")
        namelayout.addWidget(name_label)
        if kwargs['getpassword']:
            name_user = QtW.QLabel(text=kwargs['username'])
            namelayout.addWidget(name_user)
        else:
            name_field = QtW.QLineEdit()
            namelayout.addWidget(name_field)

        passwordlayout = QtW.QHBoxLayout()
        password_label = QtW.QLabel(text=" Password: ")
        password_field = QtW.QLineEdit()
        password_field.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        passwordlayout.addWidget(password_label)
        passwordlayout.addWidget(password_field)

        if kwargs['getpassword']:
            confirm_button = QtW.QPushButton(text="Confirm")

        else:
            buttonlayout = QtW.QHBoxLayout()
            cuser_button = QtW.QPushButton(
                text="Create Account")  # cuser = Create user
            cuser_button.clicked.connect(self.createuser)
            login_button = QtW.QPushButton(text="login")
            login_button.clicked.connect(lambda: self.login(
                name_field.text(),
                password_field.text()
            ))
            buttonlayout.addWidget(cuser_button)
            buttonlayout.addWidget(login_button)

        windowlayout = QtW.QVBoxLayout()
        windowlayout.addLayout(namelayout)
        windowlayout.addLayout(passwordlayout)
        if kwargs['getpassword']:
            windowlayout.addWidget(confirm_button)
        else:
            windowlayout.addLayout(buttonlayout)

        self.setLayout(windowlayout)

    def login(self, username: str, password: str):
        if self.kwargs['getpassword']:
            username = self.kwargs['username']
        if sqlf.check_password(username, password):
            if self.kwargs['getpassword']:
                self.hide()
                return True

            else:
                self.hide()
                windows['main'] = MainWindow(username)

    def createuser(self):
        windows['cuser'] = CreateUserWindow()

    def closeEvent(self, a0: QtG.QCloseEvent) -> None:
        if self.kwargs['getpassword']:
            return super().closeEvent(a0)
        exit_program()


def exit_program():
    sqlf.close()
    exit()


if __name__ == "__main__":
    app = QtW.QApplication(argv)
    windows = {'login': LoginWindow()}
    windows['login'].show()
    app.exec()
sqlf.close()
