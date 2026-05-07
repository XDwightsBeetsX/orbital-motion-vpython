"""Simple VPython orbital mechanics demo with U.S. empirical units.

Run with: python basic_orbit_simulation.py

Requires: vpython
Install with: pip install vpython
"""

import math
from vpython import canvas, sphere, vector, color, rate, cylinder, mag

# Units: miles, seconds, and miles/sec for velocity.
# Earth constants in imperial-style units.
mu_earth = 95629.33  # Earth gravitational parameter, mi^3 / s^2
R_earth = 3959.0  # Earth radius in miles

# Initial orbit parameters
altitude = 200.0  # altitude above Earth surface in miles
orbit_radius = R_earth + altitude
orbit_speed = (mu_earth / orbit_radius) ** 0.5  # circular orbit speed in mi/s

# Rocket parameters
rocket_length = 0.3 * R_earth  # visual length in miles
rocket_radius = 0.03 * R_earth  # visual radius in miles
thrust_on = True

# Setup scene
scene = canvas(title="Rocket orbiting Earth", width=900, height=700, center=vector(0, 0, 0), background=color.black)
scene.camera.pos = vector(0, -2 * orbit_radius, orbit_radius * 0.7)
scene.camera.axis = vector(0, 2 * orbit_radius, -orbit_radius * 0.7)
scene.caption = "Thrust flame animates continuously while the rocket orbits. Press 'q' to quit."

running = True

# Note: this VPython version does not support a browser-close event.
# Use the quit key instead to stop the Python process cleanly.

# Earth
earth = sphere(pos=vector(0, 0, 0), radius=R_earth, color=color.green, shininess=0.7)

# Simple rocket as a cylinder
initial_pos = vector(orbit_radius, 0, 0)
initial_axis = vector(0, 0, rocket_length)
rocket = cylinder(pos=initial_pos, axis=initial_axis, radius=rocket_radius, color=color.red, make_trail=True, trail_type="curve", interval=5, retain=300)
rocket.velocity = vector(0, orbit_speed, 0)

# Thrust flame cylinder (animated)
flame = cylinder(pos=rocket.pos, axis=-rocket.axis.norm() * rocket_length * 0.4, radius=rocket_radius * 0.6, color=color.orange, opacity=0.7, visible=thrust_on)

# Velocity direction arrow
velocity_arrow = cylinder(pos=rocket.pos, axis=rocket.velocity.norm() * R_earth * 0.25, radius=R_earth * 0.01, color=color.yellow)

# Toggle thrust and quit with keyboard
def keydown(evt):
    global thrust_on, running
    key = evt.key.lower()
    if key == 't':
        thrust_on = not thrust_on
        flame.visible = thrust_on
        print(f"Thrust {'ON' if thrust_on else 'OFF'}")
    elif key == 'q':
        running = False
        print('Quit requested. Stopping simulation.')

scene.bind('keydown', keydown)

# Simulation loop
dt = 5.0  # time step in seconds
frame = 0
while running:
    rate(100)

    # Distance vector from rocket to Earth center
    r_vec = rocket.pos
    r = mag(r_vec)

    # Gravitational acceleration toward Earth
    acceleration = -mu_earth / r**3 * r_vec

    # Update velocity and position
    rocket.velocity += acceleration * dt
    rocket.pos += rocket.velocity * dt

    # Reorient rocket to point along velocity direction
    rocket.axis = rocket.velocity.norm() * rocket_length

    # Animate thrust flame without changing the orbital dynamics
    if thrust_on:
        flame_length = rocket_length * (0.25 + 0.15 * math.sin(frame * 0.4))
        flame.axis = -rocket.axis.norm() * flame_length
        flame.color = color.orange
        flame.pos = rocket.pos

    # Update velocity arrow
    velocity_arrow.pos = rocket.pos
    velocity_arrow.axis = rocket.velocity.norm() * R_earth * 0.25

    frame += 1

    # Stop if rocket crashes into Earth
    if r <= R_earth:
        print("Rocket has impacted Earth.")
        break
