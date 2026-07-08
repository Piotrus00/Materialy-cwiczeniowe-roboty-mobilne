import event, time, cyberpi, mbot2
import time

@event.start
def on_start():
    mbot2.motor_set(50,"all")
    mbot2.straight(100)
    time.sleep(2)
    mbot2.turn(90)
    time.sleep(1)
    mbot2.straight(100)
    time.sleep(3)
    mbot2.turn(-90)
    time.sleep(1)
    mbot2.straight(100)
    time.sleep(2)
    mbot2.EM_stop("ALL")
    cyberpi.stop_all()

