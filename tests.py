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
    nums = "1,2,3,4,5,6,7,8,9,0".split(',')
    bchars = "Q,W,E,R,T,Y,U,I,O,P,A,S,D,F,G,H,J,K,L,Z,X,C,V,B,N,M".split(',')
    schars = "q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m".split(',')
    spchars = "-f_f,f.f;f:f<f>f#f&f!f?".split('f')

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
        legalcharacters = "1,2,3,4,5,6,7,8,9,0,q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m,Q,W,E,R,T,Y,U,I,O,P,A,S,D,F,G,H,J,K,L,Z,X,C,V,B,N,M,-,_".split(
            ',')
    elif charset == 'password':
        legalcharacters = "1£2£3£4£5£6£7£8£9£0£q£w£e£r£t£y£u£i£o£p£a£s£d£f£g£h£j£k£l£z£x£c£v£b£n£m£Q£W£E£R£T£Y£U£I£O£P£A£S£D£F£G£H£J£K£L£Z£X£C£V£B£N£M£-£_£,£.£;£:£<£>£#£&£!£?".split(
            '£')

    for i in string:
        if i not in legalcharacters:
            return False

    return True
