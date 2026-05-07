# Quick Start

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

Or from inside this folder:

```bash
pip install -r ../requirements.txt
```

## 3. Run the simulation

```bash
python basic_orbit_sim.py
```

## 4. Controls

- `t` — toggle thrust flame animation
- `q` — quit the simulation

## 5. Notes

- The simulation uses VPython, which opens a local browser window for visualization.
- If the window does not appear, make sure your environment supports VPython and that your browser is available.
