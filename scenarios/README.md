# Scenarios

One JSON file per scenario, loaded by the model's `ScenarioManager` (by name, via the
`LOAD_SCENARIO` command). Scenarios must be deterministic: same file → same run.

Planned backlog (from the project plan; not all will be implemented):

| File                         | Scenario |
|------------------------------|----------|
| `s01_normal_flow.json`       | Vehicle approaches on green, clear intersection |
| `s02_red_light.json`         | Vehicle stops before the stop line on red |
| `s03_pedestrian.json`        | Pedestrian requests and completes a crossing |
| `s04_multi_vehicle.json`     | Several vehicles, conflicting approaches |
| `s05_timing_change.json`     | Timing reconfigured during the run |
| `s06_v2x.json`               | Vehicle uses V2I signal information |
| `s07_comm_failure.json`      | V2X lost, fallback policy |
| `s08_perception_failure.json`| Missed/unknown detection |
| `s09_emergency_brake.json`   | Hazard ahead, emergency braking |
| `s10_high_demand.json`       | High traffic, efficiency metrics |

The file format will be fixed together with the `ScenarioManager` design.
