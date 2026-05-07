"""Earth Moon Orbit Simulation.

Run with: python earth_moon_orbit_simulation.py

Requires: vpython
Install with: pip install -r ../requirements.txt
"""

import math
import sys
from vpython import canvas, sphere, cylinder, vector, color, rate, mag

# Constants in miles and seconds
R_EARTH = 3959.0
MU_EARTH = 95629.33  # Earth gravitational parameter, mi^3/s^2
R_MOON = 1060.0
MU_MOON = 4902.8  # Moon gravitational parameter, mi^3/s^2
DIST_EARTH_MOON = 238900.0
MOON_ORBIT_SPEED = math.sqrt(MU_EARTH / DIST_EARTH_MOON)
MOON_ANGULAR_SPEED = MOON_ORBIT_SPEED / DIST_EARTH_MOON

# Visual settings
scene = canvas(
    title="Earth-Moon Orbit Simulation",
    width=1000,
    height=700,
    background=color.black,
    center=vector(DIST_EARTH_MOON * 0.5, 0, 0),
)
scene.camera.pos = vector(-0.5 * DIST_EARTH_MOON, 0.45 * DIST_EARTH_MOON, 0.30 * DIST_EARTH_MOON)
scene.camera.axis = vector(1.0 * DIST_EARTH_MOON, -0.45 * DIST_EARTH_MOON, -0.30 * DIST_EARTH_MOON)
scene.caption = "Press 'q' to quit the simulation. The rocket launches from Earth and then transitions to an orbit around the Moon."

# Earth and Moon bodies
earth = sphere(pos=vector(0, 0, 0), radius=R_EARTH, color=color.green, shininess=0.7)
moon = sphere(pos=vector(DIST_EARTH_MOON, 0, 0), radius=R_MOON, color=color.gray(0.6), shininess=0.4)

# Rocket design
rocket_length = 0.08 * R_EARTH
rocket_radius = 0.015 * R_EARTH
rocket = cylinder(
    pos=vector(R_EARTH + rocket_length * 0.5, 0, 0),
    axis=vector(0, 0, rocket_length),
    radius=rocket_radius,
    color=color.red,
    make_trail=True,
    trail_type="curve",
    interval=5,
    retain=500,
)

rocket.velocity = vector(0.0, 6.9, 0)
rocket.axis = rocket.velocity.norm() * rocket_length

running = True
simulation_time = 0.0

# Launch thrust to leave Earth and move toward the Moon
thrust_duration = 3600.0
thrust_acc = 0.0015
captured_by_moon = False
moon_capture_radius = R_MOON * 5.0
moon_orbit_radius = R_MOON * 2.5
moon_orbit_angle = 0.0

# Moon trail marker objects
moon_markers = []
max_moon_marks = 1000
moon_mark_radius = R_MOON * 0.012


def keydown(evt):
    global running
    if evt.key == 'q':
        running = False
        print('Quit requested. Stopping simulation.')

scene.bind('keydown', keydown)

# Simulation loop
minute = 60.0
hour = 60.0 * minute

dt = 10.0
moon_angle = 0.0
frame = 0

while running:
    rate(100)
    simulation_time += dt
    moon_angle += MOON_ANGULAR_SPEED * dt
    moon.pos = vector(DIST_EARTH_MOON * math.cos(moon_angle), DIST_EARTH_MOON * math.sin(moon_angle), 0)

    mark = sphere(pos=moon.pos, radius=moon_mark_radius, color=color.gray(0.6), opacity=0.4)
    moon_markers.append(mark)
    if len(moon_markers) > max_moon_marks:
        old = moon_markers.pop(0)
        old.visible = False

    if not captured_by_moon:
        r_vec = rocket.pos
        r = mag(r_vec)
        r_moon_vec = rocket.pos - moon.pos
        r_moon = mag(r_moon_vec)

        # Gravitational accelerations from Earth and Moon
        accel_earth = -MU_EARTH / r**3 * r_vec
        accel_moon = -MU_MOON / r_moon**3 * r_moon_vec

        if simulation_time <= thrust_duration:
            thrust_dir = (moon.pos - rocket.pos).norm()
            thrust = thrust_dir * thrust_acc
        else:
            thrust = vector(0, 0, 0)

        acceleration = accel_earth + accel_moon + thrust
        rocket.velocity += acceleration * dt
        rocket.pos += rocket.velocity * dt

        if mag(rocket.velocity) > 1e-6:
            rocket.axis = rocket.velocity.norm() * rocket_length

        if r <= R_EARTH:
            print('Rocket impacted Earth. Simulation ended.')
            break

        if r_moon <= R_MOON:
            print('Rocket impacted the Moon. Simulation ended.')
            break

        if r_moon <= moon_capture_radius and simulation_time > 2000.0:
            captured_by_moon = True
            rel = rocket.pos - moon.pos
            moon_orbit_radius = max(mag(rel), R_MOON * 2.2)
            moon_orbit_angle = math.atan2(rel.y, rel.x)
            rocket.velocity = vector(-rel.y, rel.x, 0).norm() * math.sqrt(MU_MOON / moon_orbit_radius)
            print('Rocket captured into Moon orbit.')
    else:
        moon_orbit_angle += math.sqrt(MU_MOON / moon_orbit_radius) / moon_orbit_radius * dt
        rel = vector(math.cos(moon_orbit_angle), math.sin(moon_orbit_angle), 0) * moon_orbit_radius
        rocket.pos = moon.pos + rel
        tangent = vector(-math.sin(moon_orbit_angle), math.cos(moon_orbit_angle), 0)
        rocket.axis = tangent.norm() * rocket_length
        rocket.velocity = tangent * math.sqrt(MU_MOON / moon_orbit_radius)

    # Keep the trail visible and update the rocket orientation
    frame += 1

    if frame % 30 == 0 and simulation_time > 10 * hour:
        scene.caption = 'Rocket continues orbiting the Moon. Press q to quit.'
