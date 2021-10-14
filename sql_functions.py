import mysql.connector
from mysql.connector import errorcode
import tests
import crypto

if __name__ == "sql_functions":
    sql = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='pythonC',
        password='TriadePadde.75',
        database='Brukersys'
    )

    cur = sql.cursor()


def close() -> None:
    sql.close()


def check_password(name: str, password: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        print(tests_list)
        return PermissionError

    try:
        cur.execute("SELECT * FROM Users WHERE username='{0}'".format(name))
        user = cur.fetchone()

        if not user[3]:  # enabled=False
            return PermissionError

        cur.execute("SELECT ukey FROM UKeys WHERE userID={0}".format(user[0]))
        key = cur.fetchone()[0]
    except:
        return ValueError

    return password == crypto.decrypt(user[2], key)


def enable_account(name: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        print(tests_list)
        return PermissionError

    # spør om passord (administrator)

    cur.execute(
        "UPDATE Users SET enabled=TRUE WHERE username='{0}'".format(name))
    return True


def disable_account(name: str) -> bool:
    # beskyttelse
    tests_list = [
        tests.using_legalcharacters(name, 'username')
    ]

    if False in tests_list:
        print(tests_list)
        return PermissionError

    # spør om passord (administrator)

    cur.execute(
        "UPDATE Users SET enabled=FALSE WHERE username='{0}'".format(name))
    return True


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
        print(tests_list)
        return PermissionError

    # kryptering
    encrypted_password, key = crypto.encrypt(password)

    # sett inn i db
    cur.execute("INSERT INTO Users (username, passwd, enabled) VALUES (%s, %s, %s)",
                (name, encrypted_password, True))
    sql.commit()

    cur.execute("SELECT id FROM Users WHERE username='{0}'".format(name))
    id = cur.fetchone()[0]

    cur.execute(
        "INSERT INTO UKeys (userID, ukey) VALUES (%s, %s)", (id, key))
    sql.commit()
    return True
