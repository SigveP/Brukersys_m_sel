from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import errorcode
import tests
import crypto

if __name__ == "sql_functions":
    sql = mysql.connector.connect(  # med rettighene 'INSERT', 'UPDATE', 'DELETE', 'SELECT'
        host='localhost',
        port='3306',
        user='pythonC',
        password='TriadePadde.75',
        database='Brukersys'
    )

    cur = sql.cursor()


def close() -> None:
    sql.close()


def log(id: str, what: str, other: str = None) -> None:
    try:
        other = get_id(other)
    except:
        other = None
    cur.execute("INSERT INTO Log (userID, what, otherID, timedone) VALUES (%s, %s, %s, %s)",
                (id, what, other, datetime.now()))
    sql.commit()


def get_id(name: str) -> None:
    cur.execute("SELECT id FROM Users WHERE username='{0}'".format(name))
    return cur.fetchone()[0]


def enable_account(name: str, id: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        return PermissionError

    cur.execute(
        "UPDATE Users SET enabled=TRUE WHERE username='{0}'".format(name))
    sql.commit()
    log(id, "enabled", name)
    return True


def disable_account(name: str, id: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        return PermissionError

    cur.execute(
        "UPDATE Users SET enabled=FALSE WHERE username='{0}'".format(name))
    sql.commit()
    log(id, "disabled", name)
    return True


def isAdministrator(id: str) -> bool:
    cur.execute(
        "SELECT * FROM Administrators WHERE userID={0}".format(id))

    try:
        assert cur.fetchone()[0] == id
        return True
    except:
        return False


def create_temporary_password(name: str, adminid: str) -> str:
    from random import choice as ranchoice

    chars = "1£2£3£4£5£6£7£8£9£0£q£w£e£r£t£y£u£i£o£p£a£s£d£f£g£h£j£k£l£z£x£c£v£b£n£m£Q£W£E£R£T£Y£U£I£O£P£A£S£D£F£G£H£J£K£L£Z£X£C£V£B£N£M£-£_£,£.£;£:£<£>£#£&£!£?".split(
        '£')

    temppass = []
    for i in range(20):
        temppass.append(ranchoice(chars))
    temppass = "".join(temppass)

    id = get_id(name)

    try:
        time = datetime.now() + timedelta(days=7)
        cur.execute(
            "INSERT INTO TempPasswords (userID, passwd, expires) VALUES (%s, %s, %s)", (id, temppass, time))
        sql.commit()
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            cur.execute(
                "SELECT passwd FROM TempPasswords WHERE userID={0}".format(id))
            return cur.fetchone()[0]
        else:
            print(err)
            return NameError
    except:
        return NameError

    log(adminid, "temporary_password", name)
    return temppass


def delete_temporary_passwords(id: str) -> None:
    cur.execute(
        "DELETE FROM TempPasswords WHERE userID={0}".format(id))
    sql.commit()


def delete_expired_temporary_passwords() -> None:
    cur.execute(
        "DELETE FROM TempPasswords WHERE expires<'{0}'".format(datetime.now()))
    sql.commit()


def change_password(id: str, new_password: str) -> bool:
    # beskyttelse
    test_list = [
        tests.between(new_password, 5, 25),
        tests.meets_requirements(new_password, 1, 1, 1, 1),
        tests.using_legalcharacters(new_password, 'password')
    ]

    if False in test_list:
        return PermissionError

    # kryptering
    encrypted_password, key = crypto.encrypt(new_password)

    # oppdatere nøkkel
    cur.execute('UPDATE UKeys SET ukey=CONVERT(\"{1}\", CHAR) WHERE userID={0}'.format(
        id, key.decode()))

    # oppdatere passord
    cur.execute("UPDATE Users SET passwd=CONVERT(\"{1}\", CHAR) WHERE id='{0}'".format(
        id, encrypted_password.decode()))

    # sletter midletidlige passord
    delete_temporary_passwords(id)

    sql.commit()
    log(id, "changed_password")
    return True


def check_password(name: str, password: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        return PermissionError

    try:
        cur.execute("SELECT * FROM Users WHERE username='{0}'".format(name))
        user = cur.fetchone()

        if not user[3]:  # enabled=False
            return PermissionError

        cur.execute("SELECT ukey FROM UKeys WHERE userID={0}".format(user[0]))
        key = cur.fetchone()[0]

        try:
            cur.execute(
                "SELECT passwd FROM TempPasswords WHERE userID={0}".format(user[0]))
            temppass = cur.fetchone()[0]
        except:
            temppass = False  # passord kan ikke være False
    except:
        return ValueError

    return password == crypto.decrypt(user[2], key) or password == temppass


def add_user(name: str, password: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.between(name, 3, 15),
        tests.meets_requirements(name, 0, 0, 1, 0),
        tests.using_legalcharacters(name, 'username'),

        tests.between(password, 5, 25),
        tests.meets_requirements(password, 1, 1, 1, 1),
        tests.using_legalcharacters(password, 'password')
    ]

    if False in tests_list:
        return PermissionError

    # kryptering
    encrypted_password, key = crypto.encrypt(password)

    # sett inn i db
    cur.execute("INSERT INTO Users (username, passwd, enabled) VALUES (%s, %s, %s)",
                (name, encrypted_password, True))
    sql.commit()

    id = get_id(name)

    cur.execute(
        "INSERT INTO UKeys (userID, ukey) VALUES (%s, %s)", (id, key))
    sql.commit()
    log(id, "create_user")
    return True
