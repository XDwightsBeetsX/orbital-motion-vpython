# VPython Projects

This repository contains two VPython demo projects that demonstrate orbital motion and launch dynamics.

## Projects

- `basic orbit simulation/` — rocket orbiting Earth with a green globe, animated thrust flame, and orbital motion visualization.
- `rocket launch simulation/` — rocket takeoff and gravity turn simulation with an automatic follow camera.

## Getting Started

1. Create and activate a Python virtual environment.

   Windows:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

   macOS / Linux:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the shared dependency.

   ```bash
   pip install -r requirements.txt
   ```

## Running the demos

- Basic orbit simulation:
  ```bash
  cd "basic orbit simulation"
  python basic_orbit_simulation.py
  ```

- Rocket launch simulation:
  ```bash
  cd "rocket launch simulation"
  python rocket_launch_simulation.py
  ```

## Files

- `requirements.txt` — Python package dependencies for all VPython projects
- `.gitignore` — ignored files for Git
- `README.md` — repository overview
- `basic orbit simulation/basic_orbit_simulation.py` — basic orbit demo script
- `basic orbit simulation/QUICKSTART.md` — quick start guide for the basic orbit demo
- `rocket launch simulation/rocket_launch_simulation.py` — rocket launch demo script
- `rocket launch simulation/QUICKSTART.md` — quick start guide for the rocket launch demo

## Requirements

- Python 3.8 or newer
- `vpython` package

## Notes

Each subfolder contains an independent VPython demo. Use the top-level `requirements.txt` once to install the dependency for both projects.
