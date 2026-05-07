# Rocket Launch Simulation

This demo shows a VPython rocket launch from take-off through a gravity turn into orbit, with a camera that follows the rocket.

## Setup

From the repository root:

```bash
pip install -r requirements.txt
```

## Run

```bash
cd "rocket launch simulation"
python rocket_launch_simulation.py
```

## Controls

- `q` — quit the simulation early

## Notes

- The VPython window will auto-focus on the rocket as it climbs and transitions into orbit.
- The simulation uses a simplified thrust profile and gravity turn for learning purposes.
- You can also run the demo from the repository root:
  ```bash
  python "rocket launch simulation/rocket_launch_simulation.py"
  ```
