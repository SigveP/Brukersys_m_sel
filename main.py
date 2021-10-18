# python 3.9.6 64-bit

import sql_functions as sqlf
import PyQt6.QtWidgets as QtW
import PyQt6.QtGui as QtG
from sys import argv
from time import time


class MainWindow(QtW.QWidget):
    def __init__(self, username, id):
        super().__init__()

        self.isadmin = sqlf.isAdministrator(id)
        self.username = username
        self.id = id
        self.last_check = time()  # hvis under 3 min: ikke spør om passord
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
        changepass_button = QtW.QPushButton(text="Change Password")
        changepass_button.clicked.connect(self.change_password)
        buttonlayout.addWidget(logout_button)
        buttonlayout.addWidget(changepass_button)

        if self.isadmin:
            adminbuttonlayout = QtW.QVBoxLayout()
            disenable_button = QtW.QPushButton("Dis/Enable Accounts")
            disenable_button.clicked.connect(self.disenable_accounts)
            changeupass_button = QtW.QPushButton(text="Temporary Passwords")
            changeupass_button.clicked.connect(self.create_temporary_password)
            adminbuttonlayout.addWidget(disenable_button)
            adminbuttonlayout.addWidget(changeupass_button)

        windowlayout = QtW.QVBoxLayout()
        windowlayout.addLayout(contentlayout)
        windowlayout.addLayout(buttonlayout)
        if self.isadmin:
            windowlayout.addLayout(adminbuttonlayout)

        self.setLayout(windowlayout)
        self.show()

    def check(self):
        t = time()

        if ((t - self.last_check) / 60) < 1:
            return True
        else:
            windows['passwordcheck'] = LoginWindow(
                getpassword=True, username=self.username)
            windows['passwordcheck'].show()

    def create_temporary_password(self):
        if self.check():
            try:
                windows['temppass'].show()
            except:
                windows['temppass'] = AdministrationWindow(
                    self.id, temppass=True)
                windows['temppass'].show()

    def disenable_accounts(self):
        if self.check():
            try:
                windows['disenable'].show()
            except:
                windows['disenable'] = AdministrationWindow(
                    self.id, disenable=True)
                windows['disenable'].show()

    def change_password(self):
        if self.check():
            windows['changepw'] = CreateUserWindow(
                changepassword=True, id=self.id)

    def logout(self):
        self.destroy()
        sqlf.log(self.id, "logout")
        windows['login'].show()

    def closeEvent(self, a0: QtG.QCloseEvent) -> None:
        exit_program()


class AdministrationWindow(QtW.QWidget):
    def __init__(self, id, **kwargs):
        super().__init__()

        self.id = id

        self.user_field = QtW.QLineEdit()

        try:
            assert kwargs['temppass']
        except:
            kwargs['temppass'] = False

        try:
            assert kwargs['disenable']
        except:
            kwargs['disenable'] = False

        if kwargs['temppass']:
            self.pass_label = QtW.QLineEdit()  # QLineEdit() så man kan kopiere
            create_button = QtW.QPushButton(text="Create")
            create_button.clicked.connect(self.createtemppass)
        elif kwargs['disenable']:
            enable_button = QtW.QPushButton(text="Enable")
            enable_button.clicked.connect(self.enableaccount)
            disable_button = QtW.QPushButton(text="Disable")
            disable_button.clicked.connect(self.disableaccount)

        layout = QtW.QVBoxLayout()
        layout.addWidget(self.user_field)
        if kwargs['temppass']:
            layout.addWidget(self.pass_label)
            layout.addWidget(create_button)
        elif kwargs['disenable']:
            layout.addWidget(enable_button)
            layout.addWidget(disable_button)

        self.setLayout(layout)

    def createtemppass(self):
        temppass = sqlf.create_temporary_password(
            self.user_field.text(), self.id)
        self.pass_label.setText(temppass)
        if temppass != NameError:
            QtW.QMessageBox.about(
                self, 'Info', 'Created TempPass for {0}'.format(self.user_field.text()))

    def enableaccount(self):
        enabled = sqlf.enable_account(self.user_field.text(), self.id)
        if enabled == PermissionError:
            errors.showMessage(
                "There was an error while trying to enable {0}".format(self.user_field.text()))
        else:
            QtW.QMessageBox.about(
                self, 'Info', 'Enabled {0}'.format(self.user_field.text()))

    def disableaccount(self):
        enabled = sqlf.disable_account(self.user_field.text(), self.id)
        if enabled == PermissionError:
            errors.showMessage(
                "There was an error while trying to disable {0}".format(self.user_field.text()))
        else:
            QtW.QMessageBox.about(
                self, 'Info', 'Disabled {0}'.format(self.user_field.text()))


class CreateUserWindow(QtW.QWidget):
    def __init__(self, **kwargs):
        super().__init__()

        try:
            assert kwargs['changepassword']
        except:
            kwargs['changepassword'] = False

        if not kwargs['changepassword']:
            namelayout = QtW.QHBoxLayout()
            name_label = QtW.QLabel(text="Username: ")
            name_field = QtW.QLineEdit()
            namelayout.addWidget(name_label)
            namelayout.addWidget(name_field)

        passwordlayout = QtW.QHBoxLayout()
        password_label = QtW.QLabel(text=" Password: ")
        if kwargs['changepassword']:
            password_label.setText("New Password: ")
        password_field = QtW.QLineEdit()
        password_field.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        passwordlayout.addWidget(password_label)
        passwordlayout.addWidget(password_field)

        rpasswordlayout = QtW.QHBoxLayout()
        rpassword_label = QtW.QLabel(text=" Password: ")
        if kwargs['changepassword']:
            rpassword_label.setText("New Password: ")
        rpassword_field = QtW.QLineEdit()
        rpassword_field.setEchoMode(QtW.QLineEdit.EchoMode.Password)
        rpasswordlayout.addWidget(rpassword_label)
        rpasswordlayout.addWidget(rpassword_field)

        if kwargs['changepassword']:
            change_button = QtW.QPushButton(text="Change Password")
            change_button.clicked.connect(lambda: self.createuser(
                kwargs['id'],
                password_field.text(),
                rpassword_field.text()
            ))
        else:
            create_button = QtW.QPushButton(text="Create Account")
            create_button.clicked.connect(lambda: self.createuser(
                name_field.text(),
                password_field.text(),
                rpassword_field.text()
            ))

        windowlayout = QtW.QVBoxLayout()
        if kwargs['changepassword']:
            windowlayout.addLayout(passwordlayout)
            windowlayout.addLayout(rpasswordlayout)
            windowlayout.addWidget(change_button)
        else:
            windowlayout.addLayout(namelayout)
            windowlayout.addLayout(passwordlayout)
            windowlayout.addLayout(rpasswordlayout)
            windowlayout.addWidget(create_button)

        self.setLayout(windowlayout)
        self.kwargs = kwargs
        self.show()

    def createuser(self, username, password, rpassword):
        if password != rpassword:
            errors.showMessage("Password do not match")
            return

        if self.kwargs['changepassword']:
            added = sqlf.change_password(username, password)
        else:
            added = sqlf.add_user(username, password)

        if added == True:
            if self.kwargs['changepassword']:
                QtW.QMessageBox.about(self, 'Info', 'Changed Password')
            else:
                QtW.QMessageBox.about(self, 'Info', 'Created Account')
            self.destroy()
        elif added == PermissionError:  # hvis feil på testene
            errors.showMessage(
                "Username or password doesn't meet the requirements")
        else:
            errors.showMessage(
                "There was an error while trying to make the account {0}".format(username))
        return


class LoginWindow(QtW.QWidget):
    def __init__(self, **kwargs):
        super().__init__()

        try:
            assert kwargs['getpassword']
        except:
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
            confirm_button.clicked.connect(lambda: self.login(
                kwargs['username'], password_field.text()))

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
        try:
            assert sqlf.check_password(username, password) == True
            if self.kwargs['getpassword']:
                windows['main'].last_check = time()
                self.destroy()

            else:
                self.hide()
                id = sqlf.get_id(username)
                sqlf.log(id, "login")
                windows['main'] = MainWindow(username, id)
        except PermissionError:
            errors.showMessage("Account is disabled")
        except:
            errors.showMessage("Wrong username or/and password!")

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
    errors = QtW.QErrorMessage()
    sqlf.delete_expired_temporary_passwords()
    windows = {'login': LoginWindow()}
    windows['login'].show()
    app.exec()
sqlf.close()
