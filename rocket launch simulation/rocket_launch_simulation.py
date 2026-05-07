"""Rocket launch simulation from take-off to orbit.

Run with: python rocket_launch_simulation.py

Requires: vpython
Install with: pip install -r ../requirements.txt
"""

import sys
import math
from vpython import canvas, sphere, cylinder, box, vector, color, rate, mag

# Units are miles and seconds.
R_earth = 3959.0  # Earth radius in miles
mu_earth = 95629.33  # Earth gravitational parameter, mi^3 / s^2

# Target orbit
target_altitude = 200.0  # miles above Earth surface
target_radius = R_earth + target_altitude
orbit_speed = math.sqrt(mu_earth / target_radius)

# Rocket geometry
rocket_length = 0.3 * R_earth
rocket_radius = 0.03 * R_earth

dt = 1.0
thrust_acc = 0.012  # miles per second squared
pitch_duration = 250.0  # seconds for gravity turn

scene = canvas(title="Rocket Launch Simulation", width=900, height=700, background=color.black)
scene.camera.pos = vector(R_earth - 1.5 * R_earth, -1.2 * R_earth, 0.8 * R_earth)
scene.camera.axis = vector(1.5 * R_earth, 1.2 * R_earth, -0.8 * R_earth)
scene.caption = "Press 'q' to quit early."

earth = sphere(pos=vector(0, 0, 0), radius=R_earth, color=color.green, shininess=0.6)
pad_thickness = 0.002 * R_earth
launch_pad = box(pos=vector(R_earth + pad_thickness / 2, 0, 0), size=vector(pad_thickness, 0.08 * R_earth, 0.02 * R_earth), color=color.gray(0.5))

rocket = cylinder(pos=vector(R_earth + pad_thickness, 0, 0), axis=vector(rocket_length, 0, 0), radius=rocket_radius, color=color.red, make_trail=True, trail_type="curve", interval=5, retain=300)
rocket.velocity = vector(0, 0, 0)
launch_direction = vector(1, 0, 0)
orbit_direction = vector(0, 1, 0)

running = True
thrust_on = True
simulation_time = 0.0


def keydown(evt):
    global running
    if evt.key == 'q':
        running = False
        print("Quit requested. Stopping simulation.")

scene.bind('keydown', keydown)

while running:
    rate(100)
    simulation_time += dt

    r_vec = rocket.pos
    r = mag(r_vec)
    gravity = -mu_earth / r**3 * r_vec

    if thrust_on:
        pitch = min(simulation_time / pitch_duration, 1.0)
        thrust_dir = (launch_direction * (1 - pitch) + orbit_direction * pitch).norm()
        thrust = thrust_dir * thrust_acc
        acceleration = gravity + thrust
        rocket.axis = thrust_dir * rocket_length
    else:
        acceleration = gravity

    rocket.velocity += acceleration * dt
    rocket.pos += rocket.velocity * dt

    if rocket.velocity.mag > 1e-6:
        rocket.axis = rocket.velocity.norm() * rocket_length

    if thrust_on and r >= target_radius and rocket.velocity.mag >= orbit_speed * 0.95:
        thrust_on = False
        print("Orbit reached. Thrust off.")

    if r <= R_earth:
        print("Rocket impacted Earth.")
        break

    scene.center = rocket.pos
    camera_offset = -rocket.axis.norm() * R_earth * 0.9 + vector(0, -0.25 * R_earth, 0.35 * R_earth)
    scene.camera.pos = rocket.pos + camera_offset
    scene.camera.axis = rocket.pos - scene.camera.pos

if not running:
    sys.exit(0)
