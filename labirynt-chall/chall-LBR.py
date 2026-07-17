import mbot2
import mbuild
import event
import time
import cyberpi


sciezka_list = []

predkosc = 1
wspolczynnik_skretu = 0.6


def line_follow(speed, steering):
    deviation = mbuild.quad_rgb_sensor.get_offset_track(1)
    left_eng = -1 * (speed + steering * deviation)
    right_eng = speed - steering * deviation
    mbot2.drive_speed(left_eng, right_eng)


skroty = {

    ('L','B','L'): 'F',
    ('L','B','F'): 'R',
    ('L','B','R'): 'B',

    ('F','B','L'): 'R',
    ('F','B','F'): 'B',
    ('F','B','R'): 'L',

    ('R','B','L'): 'B',
    ('R','B','F'): 'L',
    ('R','B','R'): 'F'

}


def optymalizuj():
    if len(sciezka_list) < 3:
        return

    ostatnie = (
        sciezka_list[-3],
        sciezka_list[-2],
        sciezka_list[-1]
    )

    if ostatnie in skroty:
        nowy_ruch = skroty[ostatnie]
        del sciezka_list[-3:]
        sciezka_list.append(nowy_ruch)


def wybor_trasy():
    line_all = mbuild.quad_rgb_sensor.get_line_sta("all",1)
    line_middle = mbuild.quad_rgb_sensor.get_line_sta("middle",1)

    # LEWO
    if line_all == 14 or line_all == 15:
        mbot2.turn(-90)
        sciezka_list.append('L')
        optymalizuj()

    # PROSTO
    elif line_all == 7:
        mbot2.straight(10)
        sciezka_list.append('F')
        optymalizuj()



    # PRAWO
    elif line_middle == 3:
        mbot2.turn(90)
        sciezka_list.append('R')
        optymalizuj()



    # ŚLEPY ZAUŁEK
    elif line_all == 0:
        mbot2.turn(-180)
        mbot2.straight(10)
        sciezka_list.append('B')
        optymalizuj()



@event.start
def on_start():

    global sciezka_list
    while True:
        line_follow(predkosc, wspolczynnik_skretu)
       
        # META NIEBIESKA
        if mbuild.quad_rgb_sensor.is_color("blue","any",1):
            mbot2.EM_stop("ALL")
            print("META")
            print(sciezka_list)
            break

        # wykrycie skrzyzowania
        stan = mbuild.quad_rgb_sensor.get_line_sta("all",1)
        if stan != 6:
            mbot2.straight(10)
            wybor_trasy()
        time.sleep(0.05)