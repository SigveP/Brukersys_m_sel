def between(string: str, min: int, max: int) -> bool:
    return min <= len(string) <= max


def notSQL(string: str) -> bool:
    sqlcmds = [  # hentet fra https://www.javatpoint.com/dbms-sql-command
        'CREATE', 'DROP', 'ALTER', 'TRUNCATE',
        'INSERT', 'UPDATE', 'DELETE',
        'GRANT', 'REVOKE',
        'COMMIT', 'ROLLBACK', 'SAVE POINT',
        'SELECT'
    ]

    try:
        string = string.split(' ')[0]
        if string.upper() in sqlcmds:
            return False
    except:
        if string.upper() in sqlcmds:
            return False

    return True


def meets_requirements(string: str, numbers: int, bigchars: int,
                       smallchars: int, specialchars: int) -> bool:
    nums = "1234567890"
    bchars = "QWERTYUIOPASDFGHJKLZXCVBNM"
    schars = "qwertyuiopasdfghjklzxcvbnm"
    spchars = "-_,.;:<>#&!?"

    counters = [0, 0, 0, 0]
    for i in string:
        if i in nums:
            counters[0] += 1
        elif i in bchars:
            counters[1] += 1
        elif i in schars:
            counters[2] += 1
        elif i in spchars:
            counters[3] += 1

    results = (
        numbers <= counters[0],
        bigchars <= counters[1],
        smallchars <= counters[2],
        specialchars <= counters[3]
    )

    return False not in results


def using_legalcharacters(string: str, charset: str) -> bool:
    if charset == 'username':
        legalcharacters = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-_"
    elif charset == 'password':
        legalcharacters = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-_,.;:<>#&!?"

    for i in string:
        if i not in legalcharacters:
            return False

    return True
