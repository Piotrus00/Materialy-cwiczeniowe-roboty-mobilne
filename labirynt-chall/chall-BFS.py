import mbot2
import mbuild
import event
import time

predkosc = 1
wspolczynnik_skretu = 0.6

graf = {(0,0): []}

pozycja = (0,0)
orientacja = "N"


# kierunki świata - dla orientacji robota
kierunki = {
    "N": (0,1),
    "E": (1,0),
    "S": (0,-1),
    "W": (-1,0)
}


def dodaj_node(pos):
    if pos not in graf:
        graf[pos] = []


def odwroc(k):
    return {
        "L":"R",
        "R":"L",
        "F":"F",
        "B":"B"
    }[k]


def dodaj_krawedz(a,b,kierunek):

    dodaj_node(a)
    dodaj_node(b)

    if b not in [x[0] for x in graf[a]]:
        graf[a].append((b,kierunek))


    if a not in [x[0] for x in graf[b]]:
        graf[b].append((a,odwroc(kierunek)))


def line_follow(speed, steering):
    deviation = mbuild.quad_rgb_sensor.get_offset_track(1)

    left = -1*(speed + steering*deviation)
    right = speed - steering*deviation

    mbot2.drive_speed(left,right)


def zmien_orientacje(k):
    global orientacja
    tab = ["N", "E", "S", "W"]

    i = tab.index(orientacja)

    if k=="R":
        i += 1

    elif k=="L":
        i -= 1

    elif k=="B":
        i += 2

    orientacja = tab[i%4]



def wykonaj_ruch(k):
    global pozycja

    if k=="L":
        mbot2.turn(-90)

    elif k=="R":
        mbot2.turn(90)

    elif k=="B":
        mbot2.turn(180)


    mbot2.straight(10)
    zmien_orientacje(k)
    dx,dy = kierunki[orientacja]

    pozycja = (pozycja[0]+dx, pozycja[1]+dy)


def bfs(start,cel):
    kolejka=[start]
    rodzic={
        start:None
    }


    while kolejka:
        obecny=kolejka.pop(0)

        if obecny==cel:
            break

        for sasiad,kierunek in graf[obecny]:
            if sasiad not in rodzic:
                rodzic[sasiad]=obecny
                kolejka.append(sasiad)


    if cel not in rodzic:
        return None

    trasa=[]
    x=cel
    while x:
        trasa.append(x)
        x=rodzic[x]

    trasa.reverse()
    return trasa


# szukanie ruchu z wierzchołka a do b w grafie
def znajdz_kierunek(a,b):
    for s,k in graf[a]:
        if s==b:
            return k
    return None



def przejedz_trase(trasa):
    for i in range(len(trasa)-1):

        k = znajdz_kierunek(trasa[i], trasa[i+1])

        wykonaj_ruch(k)
        time.sleep(0.2)


def wybor_trasy():

    global pozycja
    stan = mbuild.quad_rgb_sensor.get_line_sta("all",1)
    stara = pozycja
    dx,dy = kierunki[orientacja]

    if stan==14 or stan==15:
        nowa = (pozycja[0]-dy, pozycja[1]+dx)
        dodaj_krawedz(stara, nowa, "L")
        wykonaj_ruch("L")

    elif stan==7:
        nowa=(pozycja[0]+dx, pozycja[1]+dy)
        dodaj_krawedz(stara, nowa, "F")
        wykonaj_ruch("F")

    elif stan==3:
        nowa=(pozycja[0]+dy, pozycja[1]-dx)
        dodaj_krawedz(stara, nowa, "R")
        wykonaj_ruch("R")


    elif stan==0:
        nowa=(pozycja[0]-dx, pozycja[1]-dy)
        dodaj_krawedz(stara, nowa, "B")
        wykonaj_ruch("B")




@event.start
def on_start():

    while True:
        line_follow(predkosc, wspolczynnik_skretu)

        if mbuild.quad_rgb_sensor.is_color("blue", "any", 1):
            mbot2.EM_stop("ALL")
            cel=pozycja
            trasa=bfs((0,0), cel)

            przejedz_trase(trasa)

            break

        stan=mbuild.quad_rgb_sensor.get_line_sta("all", 1)

        if stan!=6:
            wybor_trasy()

        time.sleep(0.05)
