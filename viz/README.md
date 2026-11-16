# Python visualization

Pygame front end with three panels:

1. **Configuration** — signal timings, vehicle speed, scenario, start/pause/reset.
2. **Telemetry** — selected vehicle's speed, state, perceived vs actual light,
   detections, V2X link, event log.
3. **Map** — top-down intersection; vehicles as rectangles, pedestrians as X.

## Rules

- Renders what the model sends. It never moves a vehicle, changes a light or decides
  a crossing on its own.
- May interpolate positions between two received states for smoother drawing.
- Configuration changes are sent as commands and only shown as applied after the
  model's `ack` says `accepted: true`.

## Layout

```
viz/
├── requirements.txt
├── smart_intersection_viz/
│   ├── __main__.py      entry point (python -m smart_intersection_viz)
│   ├── net.py           UDP receive/send, JSON + schema checks
│   ├── world.py         world (m) ↔ screen (px) transform
│   └── panels/          config_panel.py, telemetry_panel.py, map_panel.py
└── tests/
```

## Run

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m smart_intersection_viz
```
