import mbot2, mbuild, event, time, cyberpi
import time

# initialize variables
srodkowanie = 0
cross_count = 0
prog = 0
cross_type = 0
predkosc = 0
wspolczynnik_skretu = 0
left_eng = 0
right_eng = 0


def line_follow_N_N_N(speed, steering, sensor):
    global srodkowanie, cross_count, prog, cross_type, predkosc, wspolczynnik_skretu, left_eng, right_eng
    left_eng = speed - steering * sensor
    right_eng = ((speed + steering * sensor)) * -1
    mbot2.EM_set_speed(left_eng, "EM1")
    mbot2.EM_set_speed(right_eng, "EM2")


def cross_logic():
    global srodkowanie, cross_count, prog, cross_type, predkosc, wspolczynnik_skretu, left_eng, right_eng

    temp = mbuild.quad_rgb_sensor.get_line_sta("all", 1)

    if cross_type == temp:
        cross_count = cross_count + 1

    else:
        cross_count = 0

    cross_type = temp


def red_check():
    if mbuild.quad_rgb_sensor.is_color("red", "any", 1):
        cyberpi.audio.play_until("meow")
        mbot2.turn(-360)
        cyberpi.led.show("red red red red red")
        time.sleep(1)
        cyberpi.stop_all()


def smooth_u_turn():
    mbot2.motor_stop("all")
    time.sleep(0.1)
    mbot2.EM_set_speed(30, "EM1")
    mbot2.EM_set_speed(30, "EM2")
    while not (mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 6):
        pass

    mbot2.motor_stop("all")


@event.start
def on_start():
    global srodkowanie, cross_count, prog, cross_type, predkosc, wspolczynnik_skretu, left_eng, right_eng
    srodkowanie = 6.7
    cross_count = 0
    prog = 5
    cross_type = 0
    predkosc = 25
    wspolczynnik_skretu = 0.6
    while True:
        red_check()
        # LEWO
        if mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 14:
            cross_logic()
            if cross_count == prog:
                mbot2.motor_stop("all")
                mbot2.straight(srodkowanie)
                mbot2.motor_stop("all")
                time.sleep(0.2)
                mbot2.turn(-90)
                cross_count = 0

        # T lub +
        if mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 15:
            cross_logic()
            if cross_count == prog:
                mbot2.motor_stop("all")
                mbot2.straight(srodkowanie)
                mbot2.motor_stop("all")
                time.sleep(0.2)

                # +
                if mbuild.quad_rgb_sensor.get_line_sta("all", 1) != 0:
                    mbot2.turn(-90)
                    cyberpi.audio.play("meow")
                    cross_count = 0
                # T
                else:
                    mbot2.turn(-90)
                    cyberpi.audio.play("annoyed")
                    cross_count = 0
        # PRAWO
        if mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 7:
            cross_logic()
            if cross_count == prog:
                mbot2.motor_stop("all")
                time.sleep(0.2)
                mbot2.straight(srodkowanie)
                mbot2.motor_stop("all")
                time.sleep(0.2)
                # skret w prawo
                if mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 0:
                    mbot2.turn(90)
                cross_count = 0
            # SLEPY
        if mbuild.quad_rgb_sensor.get_line_sta("all", 1) == 0:
            smooth_u_turn()
        line_follow_N_N_N(
            predkosc, wspolczynnik_skretu, mbuild.quad_rgb_sensor.get_offset_track(1)
        )
