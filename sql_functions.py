from configparser import Error
from datetime import datetime
import mysql.connector
from mysql.connector import errorcode
import crypto

if __name__ == "sql_functions":
    sql = mysql.connector.connect(
        host='',
        port='',
        user='',
        password='',
        database=''
    )

    cur = sql.cursor()


def close() -> None:
    sql.close()


def enable_account(name: str, accesstime: datetime) -> bool:
    # beskyttelse
    # ...

    # spør om passord (administrator)

    cur.execute(
        "UPDATE Users SET enabled=TRUE WHERE username='{0}'".format(name))
    return True


def disable_account(name: str) -> bool:
    # beskyttelse
    # ...

    # spør om passord (administrator)

    cur.execute(
        "UPDATE Users SET enabled=FALSE WHERE username='{0}'".format(name))
    return True


def check_password(name: str, password: str) -> bool:
    # beskyttelse
    # ...

    try:
        cur.execute("SELECT * FROM Users WHERE username='{0}'".format(name))
        user = cur.fetchone()

        if not user[3]:  # enabled=False
            return PermissionError

        cur.execute("SELECT ukey FROM UKeys WHERE userID={0}".format(user[0]))
        key = cur.fetchone()[0]
    except:
        return Error

    return password == crypto.decrypt(user[2], key)


def add_user(name: str, password: str) -> bool:
    # beskyttelse
    # ...

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
