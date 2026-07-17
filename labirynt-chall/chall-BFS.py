import mbot2
import mbuild
import event
import time

predkosc = 1
wspolczynnik_skretu = 0.6

# graf[node] = [(sasiad, dystans, kierunek)]
graf = {0: []}

aktualny_node = 0


def line_follow(speed, steering):
    deviation = mbuild.quad_rgb_sensor.get_offset_track(1)

    left_eng = -1 * (speed + steering * deviation)
    right_eng = speed - steering * deviation

    mbot2.drive_speed(left_eng, right_eng)


def dodaj_node():
    nowy = len(graf)
    graf[nowy] = []
    return nowy


def dodaj_krawedz(a, b, dystans, kierunek):
    odwrotny = {
        "L": "R",
        "R": "L",
        "F": "F",
        "B": "B"
    }

    if b not in [x[0] for x in graf[a]]:
        graf[a].append((b, dystans, kierunek))

    if a not in [x[0] for x in graf[b]]:
        graf[b].append((a, dystans, odwrotny[kierunek]))


def bfs(start, cel):
    kolejka = [start]
    odwiedzone = {start}
    rodzic = {start: None}

    while kolejka:
        aktualny = kolejka.pop(0)

        if aktualny == cel:
            break

        for sasiad, dystans, kierunek in graf[aktualny]:
            if sasiad not in odwiedzone:
                odwiedzone.add(sasiad)
                rodzic[sasiad] = aktualny
                kolejka.append(sasiad)
    
    if cel not in rodzic:
        return None
    sciezka = []
    node = cel
    while node is not None:
        sciezka.append(node)
        node = rodzic[node]
    sciezka.reverse()
    return sciezka


def wybor_trasy():
    global aktualny_node

    line_all = mbuild.quad_rgb_sensor.get_line_sta("all", 1)
    line_middle = mbuild.quad_rgb_sensor.get_line_sta("middle", 1)

    stary = aktualny_node
    nowy = dodaj_node()

    if line_all == 14 or line_all == 15:
        kierunek = "L"
        dodaj_krawedz(stary, nowy, 10, kierunek)
        mbot2.turn(-90)

    elif line_all == 7:
        kierunek = "F"
        dodaj_krawedz(stary, nowy, 10, kierunek)
        mbot2.straight(10)

    elif line_middle == 3:
        kierunek = "R"
        dodaj_krawedz(stary, nowy, 10, kierunek)
        mbot2.turn(90)

    elif line_all == 0:
        kierunek = "B"

        dodaj_krawedz(stary, nowy, 10, kierunek)

        mbot2.turn(-180)
        mbot2.straight(10)

    aktualny_node = nowy


@event.start
def on_start():
    while True:
        line_follow(predkosc, wspolczynnik_skretu)
        if mbuild.quad_rgb_sensor.is_color("blue", "any", 1):
            mbot2.EM_stop("ALL")
            print("MAPA GRAFU:")
            for node in graf:
                print(node, "->", graf[node])

            cel = len(graf) - 1
            trasa = bfs(0, cel)
            print("BFS TRASA:", trasa)
            break

        stan = mbuild.quad_rgb_sensor.get_line_sta("all", 1)
        if stan != 6:
            wybor_trasy()

        time.sleep(0.05)
