import event, time, cyberpi, mbuild, mbot2
import time

@event.is_press('a')
def is_btn_press():
    cyberpi.audio.record()
    time.sleep(3)
    cyberpi.audio.stop_record()

@event.is_press('b')
def is_btn_press1():
    while True:
      if mbuild.ultrasonic2.get(1) < 20:
        mbot2.motor_stop("all")
        cyberpi.audio.play_record()
        mbot2.turn(-180)

      else:
        mbot2.forward(50)

