# Earth Moon Orbit Simulation

This demo launches a rocket from Earth and simulates a looping path around the Moon and Earth in a figure-eight style trajectory.

## 1. Create or activate your Python environment

Using `venv`:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Using `conda`:

```bash
conda create -n orbital-motion python=3.10
conda activate orbital-motion
```

## 2. Install dependencies

From the repository root:

```bash
pip install -r requirements.txt
```

## 3. Run the simulation

```bash
cd "earth moon orbit simulation"
python earth_moon_orbit_simulation.py
```

## Controls

- `q` — quit the simulation

## Notes

- The Moon is represented as a smaller gray sphere orbiting Earth.
- The camera remains fixed for this demo, so the Earth, Moon, and rocket motion are visible together.
- If the VPython window does not appear, ensure your environment supports VPython and that your browser is available.
