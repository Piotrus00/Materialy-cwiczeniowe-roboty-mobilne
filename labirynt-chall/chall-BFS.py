import mbot2
import mbuild
import event
import time
import cyberpi

predkosc = 1
wspolczynnik_skretu = 0.6

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

def dodaj_krawedz(a, b, dystans):
    if b not in [x[0] for x in graf[a]]:
        graf[a].append((b, dystans))
    if a not in [x[0] for x in graf[b]]:
        graf[b].append((a, dystans))

def wybor_trasy():
    global aktualny_node

    line_all = mbuild.quad_rgb_sensor.get_line_sta("all",1)
    line_middle = mbuild.quad_rgb_sensor.get_line_sta("middle",1)

    stary = aktualny_node
    nowy = dodaj_node()

    dodaj_krawedz(stary, nowy, 10)

    aktualny_node = nowy

    if line_all == 14 or line_all == 15:
        mbot2.turn(-90)
    elif line_all == 7:
        mbot2.straight(10)
    elif line_middle == 3:
        mbot2.turn(90)
    elif line_all == 0:
        mbot2.turn(-180)
        mbot2.straight(10)

@event.start
def on_start():
    while True:
        line_follow(predkosc, wspolczynnik_skretu)

        if mbuild.quad_rgb_sensor.is_color("blue","any",1):
            mbot2.EM_stop("ALL")
            print(graf)
            break

        stan = mbuild.quad_rgb_sensor.get_line_sta("all",1)

        if stan != 6:
            wybor_trasy()

        time.sleep(0.05)
