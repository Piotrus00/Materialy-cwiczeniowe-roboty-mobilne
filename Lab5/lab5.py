import mbot2, event, time, cyberpi, mbuild
import time
# initialize variables
left_eng = 0
right_eng = 0
velocity = 0

def line_follow_proportional_N_N_N(speed, steering, deviation):
    global left_eng, right_eng, velocity
    left_eng = (speed - steering * deviation)
    right_eng = -1 * (speed + steering * deviation)
    mbot2.drive_speed(left_eng, right_eng)

@event.start
def on_start():
    global left_eng, right_eng, velocity
    velocity = 50
    while True:
      line_follow_proportional_N_N_N(velocity, 0.6, mbuild.quad_rgb_sensor.get_offset_track(1))
      if (mbuild.quad_rgb_sensor.is_color("red","any",1)):
        mbot2.EM_stop("ALL")
        cyberpi.audio.play('meow')
        time.sleep(3)
        mbot2.straight(3)

      if (mbuild.quad_rgb_sensor.is_color("green","any",1)):
        velocity = 20
        mbot2.straight(3)

      if (mbuild.quad_rgb_sensor.is_color("blue","any",1)):
        velocity = 50
        mbot2.straight(3)
        