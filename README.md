# Smart Intersection Management System

**2IN70 – Software Engineering for Autonomous Systems · TU/e · Group 7**

A model-based smart intersection simulation in which smart vehicles, pedestrians and
traffic lights interact through configurable signal control, simulated perception and
V2X communication.

> Smart vehicles and pedestrians need safe, predictable, and efficient passage through a
> shared intersection under changing traffic conditions.

## Architecture in one picture

```
 ┌──────────────────────────────┐     state (UDP/JSON)     ┌──────────────────────────┐
 │  IBM Rhapsody 9.0 model      │ ───────────────────────► │  Python / Pygame viz     │
 │  (generated C++ + bridge/)   │                          │  config · telemetry · map│
 │  ALL system behaviour lives  │ ◄─────────────────────── │  display + config ONLY   │
 │  here                        │   commands (UDP/JSON)    │                          │
 └──────────────────────────────┘                          └──────────────────────────┘
```

**Rule:** Python never decides when a light changes or a vehicle stops. It displays state
and sends requests; the Rhapsody model validates and applies them.

## Repository layout

| Folder        | Contents |
|---------------|----------|
| `model/`      | Rhapsody project (`SmartIntersection.rpyx` + `SmartIntersection_rpy/`). Source of truth for behaviour. |
| `bridge/`     | Hand-written C++ (UDP link, JSON serialisation, command parsing) pulled into the Rhapsody build. |
| `protocol/`   | Message contract between C++ and Python (JSON schemas + conventions). |
| `viz/`        | Python Pygame application (three panels). |
| `scenarios/`  | Scenario definitions (JSON) for repeatable runs. |
| `tools/`      | Dev helpers: mock simulator, demo launch script. |
| `tests/`      | Verification test cases traced to requirements, and their results. |
| `docs/`       | Submitted milestone PDFs, draw.io diagrams, decision records. |

The report itself is written in Overleaf and is **not** stored here.

## Team and ownership

| Area | Owner |
|------|-------|
| Model: Requirements, Architecture | shared |
| Model: TrafficControl, Pedestrians, Simulation | Member A *(fill in)* |
| Model: Vehicles, V2X | Member B *(fill in)* |
| `bridge/` + `protocol/` | Member B *(fill in)* |
| `viz/` | Member A *(fill in)* |
| `tests/` | shared |

Before editing a model package you don't own, tell the owner. Model files cannot be
merged safely (see `model/README.md`).

## Working agreement

- `main` must always open in Rhapsody and build.
- Work on a branch: `model/<topic>`, `feature/<topic>`, `docs/<topic>`, `fix/<topic>`.
- Merge through a pull request reviewed by the other member.
- Submitted milestones are tagged: `milestone-1`, `milestone-2`, …
- Don't commit generated code, build output, virtual environments or videos.

## Getting started

### Rhapsody model
Open `model/SmartIntersection.rpyx` in Rhapsody 9.0 (C++). Build instructions: `model/README.md`.

### Visualization
```bat
cd viz
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m smart_intersection_viz
```

### Without Rhapsody (viz development only)
```bat
python tools\mock_sim.py
```

## Status

Repository skeleton only. Nothing in this repo is implemented or tested yet; see the
GitHub issues for the development backlog.
