import event, time, cyberpi, mbuild, mbot2, random
# initialize variables
direction = 0

@event.start
def on_start():
    global direction
    while True:
      if (mbuild.quad_rgb_sensor.is_color("blue","any",1)):
        cyberpi.mesh_broadcast.set("blue", 0)
        cyberpi.led.on(1, 50, 208, "all")
        cyberpi.audio.play('score')
        mbot2.turn(-360)
        mbot2.EM_stop("ALL")
        cyberpi.stop_this()

      if mbuild.ultrasonic2.get(1) < 15:
        mbot2.turn(90)
        random_moves()

      else:
        random_moves()

def random_moves():
    global direction
    direction = random.randint(1, 2)
    if direction == 1:
      mbot2.forward(50, 1)
      mbot2.turn(-120)

    if direction == 2:
      mbot2.forward(50, 1)
      mbot2.turn(120)

@cyberpi.event.mesh_broadcast("blue")
def on_mesh_broadcast():
    global direction
    mbot2.EM_stop("ALL")
    cyberpi.led.on(208, 0, 0, "all")
    cyberpi.audio.play_until('sad')
    cyberpi.stop_this()

