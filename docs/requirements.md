# System requirements — v1.0

*Smart Intersection Simulation System · 2IN70 Group 7 · 2026-11-20 · Milestone 2*

> [!NOTE]
> Generated from [`tools/requirements/requirements.json`](../tools/requirements/requirements.json) by `tools/requirements/render.py` — edit the JSON, not this file. The same JSON is loaded into the Rhapsody `Requirements` package by `tools/requirements/rhapsody_import.py`.

## Conventions

- **Subject.** In every requirement, 'the system' is the system of interest, the block SmartIntersectionCore.
- **Syntax.** Every requirement follows one EARS template: *Ubiquitous* (The system shall …), *State-driven* (While …, the system shall …), *Event-driven* (When …, the system shall …), *Unwanted behaviour* (If …, then the system shall …), *Optional feature* (Where …, the system shall …) or *Complex* (While …, when …, the system shall …). Exactly one *shall* per requirement; no *should / will / may*; units are SI.
- **Priority (MoSCoW).** M = must, S = should, C = could.
- **Verification.** Test, Analysis, Inspection or Demonstration.
- **Source.** Stakeholder (Milestone 1, revised 16 Nov), check T1–T5 and conflict C1–C4 the requirement comes from.
- **Refined by.** Use cases (UC1–UC5) that refine the requirement with «refine» in the Rhapsody model.

**36 requirements:** 23 functional, 7 non-functional, 6 ODD · 5 unwanted-behaviour · 29 M / 6 S / 1 C.

## Use cases

| ID | Use case | Primary actor | Actor's goal |
|---|---|---|---|
| UC1 | ConfigureScenario | ScenarioOperator | Set up a scenario (traffic demand, road users, signal timing) that the system accepts as valid. |
| UC2 | RunIntersection | ScenarioOperator | Start, pause and reset a run in which the system moves road users and switches signals safely. |
| UC3 | InspectTelemetry | ScenarioOperator | Understand what the simulation is doing and why, from live state, events and metrics. |
| UC4 | ExecuteTestRun | ScenarioTestHarness | Run a scenario repeatably and obtain traces and results for verification. |
| UC5 | SubmitPerceptionDetections | MLPerceptionService | Deliver detections to the smart vehicle and get them acknowledged (planned extension). |

## Requirement structure (containment)

```
SIS  System requirements (SmartIntersectionCore)
├── FUN  Functional requirements
│   ├── SIG  Traffic signal control  (SIG-01 … SIG-05)
│   ├── RUN  Scenario and run control  (RUN-01 … RUN-07)
│   ├── AGT  Road-user behaviour  (AGT-01 … AGT-04)
│   ├── SV   Smart-vehicle perception and decision  (SV-01 … SV-04)
│   └── OBS  Telemetry and evaluation  (OBS-01 … OBS-03)
├── NFR  Non-functional requirements  (NFR-01 … NFR-07)
└── ODD  Operational design domain  (ODD-01 … ODD-06)
```

## SIG — Traffic signal control

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **SIG-01** | Ubiquitous | The system shall switch the vehicle signals in the repeating sequence N/S green, N/S amber, all-red, E/W green, E/W amber, all-red. | Two mutually exclusive movement groups with amber and all-red clearance is the signal plan of the ODD; all other signal requirements assume this order. | Road authority; conventional drivers | M | Test | UC2 |
| **SIG-02** | State-driven | While a vehicle movement group shows green or amber, the system shall show red to the other vehicle movement group. | Primary safety invariant: conflicting vehicle movements never have permission at the same time. | Road authority; occupants; drivers; check T1 | M | Test | UC2 |
| **SIG-03** | State-driven | While a pedestrian crossing shows walk or pedestrian clearance, the system shall show red to every vehicle movement group that crosses it. | Protected pedestrian permission: a pedestrian on the crossing is never in conflict with a permitted vehicle movement. | Pedestrians; road authority; check T1; conflict C1 | M | Test | UC2 |
| **SIG-04** | Event-driven | When a pedestrian agent requests to cross, the system shall show walk on that crossing in the next phase in which every vehicle movement group that crosses it shows red. | Bounds the pedestrian waiting time to at most one signal cycle while respecting SIG-03. | Pedestrians; conflict C2 | M | Test | UC2 |
| **SIG-05** | Ubiquitous | The system shall give every pedestrian clearance interval a duration of at least the crossing length divided by 0.8 m/s. | The slowest pedestrian in the ODD (0.8 m/s) can finish crossing before a conflicting vehicle movement receives green. | Pedestrians; road authority; conflict C2 | M | Analysis | UC1, UC2 |

## RUN — Scenario and run control

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **RUN-01** | Event-driven | When the system receives a load-scenario command, the system shall initialise the road geometry, agents, arrival times, timing plan and random seed from that scenario. | All inputs that determine a run come from one scenario, which makes runs repeatable and comparable. | Operator; course team; check T4 | M | Test | UC1, UC4 |
| **RUN-02** | Unwanted behaviour | If a requested signal duration is outside its permitted range (green 5–60 s, amber 2–5 s, all-red 1–3 s, walk 5–30 s), then the system shall reject the request and report the permitted range. | An out-of-range duration could create an unsafe or unrealistic plan; reporting the range lets the operator correct the request. | Road authority; operator; check T3; conflict C3 | M | Test | UC1 |
| **RUN-03** | State-driven | While an accepted timing plan is pending, the system shall keep the active timing plan until the next all-red interval starts. | A timing change can then never shorten an active green, amber or pedestrian clearance interval. | Road authority; pedestrians; check T3; conflict C3 | M | Test | UC1, UC2 |
| **RUN-04** | Event-driven | When the system receives an operator command, the system shall acknowledge the command as accepted, or as rejected with a reason, within one simulation step. | The dashboard only requests changes and the model decides; an explicit acknowledgement shows the operator which value is active. | Operator; conflict C3 | M | Test | UC1, UC2 |
| **RUN-05** | Event-driven | When the system receives a reset command, the system shall restore the initial state of the loaded scenario. | The operator can repeat a run without reloading, e.g. to compare two timing plans on the same traffic. | Operator / researcher | S | Test | UC2 |
| **RUN-06** | State-driven | While a run is paused, the system shall keep the simulation time and the state of every signal and agent unchanged. | Pausing freezes the whole model, so the operator can inspect a situation without the state moving on. | Operator | M | Test | UC2 |
| **RUN-07** | Complex (state + event) | While a run is paused, when the system receives a step command, the system shall advance the simulation by exactly one simulation step. | Step-wise execution lets the team inspect each state-machine transition during debugging and the demonstration. | Course team; operator | S | Test | UC2 |

## AGT — Road-user behaviour

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **AGT-01** | Ubiquitous | The system shall update the position and speed of every agent once per simulation step. | Agent motion is owned by the model, not by the dashboard, and is consistent with the fixed time step (NFR-02). | Course team | M | Test | UC2 |
| **AGT-02** | State-driven | While an approach shows red, the system shall keep every vehicle agent on that approach that has not passed the stop line behind the stop line. | Red-light compliance of every vehicle, smart and conventional. | Occupants; drivers; road authority; check T2; conflict C1 | M | Test | UC2 |
| **AGT-03** | Event-driven | When an approach changes to amber, the system shall stop every vehicle agent on that approach that can stop before the stop line with a deceleration of at most 4.5 m/s². | Vehicles that can stop comfortably do so and vehicles too close to stop proceed; with amber of at least 2 s and speed of at most 8.5 m/s this makes AGT-02 achievable. | Occupants (braking within limits); drivers; conflict C1 | M | Test | UC2 |
| **AGT-04** | Ubiquitous | The system shall start a pedestrian agent across a crossing only while that crossing shows walk. | Pedestrians in the ODD comply with the signals, so their safety follows from SIG-03. | Pedestrians; conflict C1 | M | Test | UC2 |

## SV — Smart-vehicle perception and decision

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **SV-01** | Ubiquitous | The system shall base every stop, yield or proceed decision of the smart vehicle on the smart vehicle's observed state of signals, vehicles and pedestrians. | Makes the perception-to-decision chain explicit and testable, as for a real automated vehicle. | Smart-vehicle developers; occupants; conflict C4 | M | Test | UC2, UC5 |
| **SV-02** | Ubiquitous | The system shall store the smart vehicle's observed state separately from the simulated ground truth. | A perception error can then be detected by comparing observation with ground truth instead of being hidden. | Smart-vehicle developers; course team; conflict C4 | M | Inspection | UC3 |
| **SV-03** | Unwanted behaviour | If the smart vehicle's latest observation of its signal is missing, older than 0.5 s or has a confidence below 0.8, then the system shall treat that signal as red for the smart vehicle. | Fail-safe interpretation of uncertain perception: an unconfirmed green is never acted upon. Thresholds are proposed values. | Occupants; pedestrians; check T5; conflict C4 | S | Test | UC5, UC2 |
| **SV-04** | Optional feature | Where the ML perception service is connected, the system shall accept time-stamped detection events containing object class, signal indication and confidence through the perception interface. | Enables the planned ML extension without making it a dependency of the baseline. | Smart-vehicle developers; conflict C4 | C | Test | UC5 |

## OBS — Telemetry and evaluation

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **OBS-01** | Ubiquitous | The system shall publish a state snapshot every simulation step containing the simulation time, the active phase, every signal indication, and the id, type, position, speed and state of every agent. | The dashboard displays only model-owned state; a complete snapshot every step means a lost message is replaced by the next one. | Operator; course team | M | Test | UC3, UC2 |
| **OBS-02** | Event-driven | When a phase change, operator command, vehicle stop at a stop line, crossing request, crossing completion or safety-rule violation occurs, the system shall record a time-stamped event in the run log. | The event log is the evidence for verification (checks T1–T4) and the basis for comparing runs. | Course team; road authority | M | Test | UC3, UC4 |
| **OBS-03** | Event-driven | When a run ends, the system shall report the waiting time of every agent, the maximum queue length per arm and the number of vehicle stops. | Quantifies the delay-versus-safety trade-off between timing plans. | Operator / researcher; road authority; drivers; check T4; conflicts C1, C2 | S | Test | UC4, UC3 |

## NFR — Non-functional requirements

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **NFR-01** | Ubiquitous | The system shall produce identical event logs for any two runs of the same scenario with the same random seed and timing plan. | A difference between two runs can then be attributed to the changed parameter only. | Operator; course team; check T4; conflict C3 | M | Test | UC4 |
| **NFR-02** | Ubiquitous | The system shall advance the simulation time in fixed steps of 0.1 s. | A fixed step makes behaviour deterministic and gives 10 snapshots per simulated second for the dashboard. | Course team; operator | M | Test | UC2 |
| **NFR-03** | Ubiquitous | The system shall take every signal, movement and right-of-way decision inside the executable Rhapsody model. | Rhapsody is the single source of truth; external tools may only request changes, which keeps behaviour traceable to the SysML model. | Course team; conflict C3 | M | Inspection | — (system-wide) |
| **NFR-04** | Unwanted behaviour | If the system receives a message that does not conform to the interface schema, then the system shall discard the message, log a diagnostic event and continue the run. | Faulty input from the dashboard, the test harness or the ML service must not stop or corrupt the simulation. | Course team; operator | M | Test | UC1, UC4, UC5 |
| **NFR-05** | Unwanted behaviour | If the connection to the dashboard is lost during a run, then the system shall continue the run without loss of simulation state. | The dashboard is only a viewer; closing or restarting it must not affect the run. | Operator; course team | S | Test | UC2, UC3 |
| **NFR-06** | State-driven | While animation is enabled, the system shall display the active state of every signal and agent state machine in Rhapsody animation. | Makes the executable behaviour inspectable for debugging and for the live demonstration. | Course team | M | Demonstration | UC2 |
| **NFR-07** | Ubiquitous | The system shall allow the perception source of the smart vehicle to be switched between idealized and ML-based perception without modification of its decision logic. | The decision logic is verified once with idealized input and reused unchanged with ML input. | Smart-vehicle developers; conflict C4 | S | Inspection | UC5 |

## ODD — Operational design domain

| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |
|---|---|---|---|---|---|---|---|
| **ODD-01** | Ubiquitous | The system shall represent one four-arm signalized intersection with right-hand traffic, one inbound and one outbound lane per arm, a stop line on each inbound lane and one pedestrian crossing per arm. | Fixes the road geometry of the ODD, so that every conflict between movements is known in advance and can be checked exhaustively. | Road authority; course team | M | Inspection | UC1 |
| **ODD-02** | Ubiquitous | The system shall simulate at most 4 vehicle agents, of which at most 1 is a smart vehicle, and at most 6 pedestrian agents at the same time. | Enough road users for interactions between the smart vehicle, conventional vehicles and pedestrians, while keeping the state space and the test effort bounded. | Course team (manageable complexity) | M | Test | UC1, UC2 |
| **ODD-03** | Ubiquitous | The system shall move vehicle agents straight through the intersection only, without turning, overtaking or reversing. | Limits the conflicts to the two crossing movement groups; turning movements are a planned extension. | Course team; road authority | M | Inspection | UC2 |
| **ODD-04** | Ubiquitous | The system shall keep the speed of every vehicle agent between 0 m/s and 8.5 m/s. | 8.5 m/s (about 30 km/h) is a typical urban approach speed and bounds the stopping distance used in AGT-03. | Road authority; occupants | M | Test | UC2 |
| **ODD-05** | Ubiquitous | The system shall move every pedestrian agent at a walking speed between 0.8 m/s and 1.8 m/s. | Covers slow (vulnerable) to fast pedestrians; the lower bound sets the minimum clearance time of SIG-05. | Pedestrians | M | Test | UC2 |
| **ODD-06** | Unwanted behaviour | If a scenario specifies a road-user type, movement, speed or number of agents outside the limits of ODD-01 to ODD-05, then the system shall reject the scenario and report every violated limit. | Guarantees that every run stays inside the domain for which the model is designed and verified. | Road authority; operator; course team; conflict C3 | M | Test | UC1, UC4 |

## Traceability: requirement ↔ use case («refine»)

| Req. | UC1 | UC2 | UC3 | UC4 | UC5 |
|---|---|---|---|---|---|
| SIG-01 |  | ● |  |  |  |
| SIG-02 |  | ● |  |  |  |
| SIG-03 |  | ● |  |  |  |
| SIG-04 |  | ● |  |  |  |
| SIG-05 | ● | ● |  |  |  |
| RUN-01 | ● |  |  | ● |  |
| RUN-02 | ● |  |  |  |  |
| RUN-03 | ● | ● |  |  |  |
| RUN-04 | ● | ● |  |  |  |
| RUN-05 |  | ● |  |  |  |
| RUN-06 |  | ● |  |  |  |
| RUN-07 |  | ● |  |  |  |
| AGT-01 |  | ● |  |  |  |
| AGT-02 |  | ● |  |  |  |
| AGT-03 |  | ● |  |  |  |
| AGT-04 |  | ● |  |  |  |
| SV-01 |  | ● |  |  | ● |
| SV-02 |  |  | ● |  |  |
| SV-03 |  | ● |  |  | ● |
| SV-04 |  |  |  |  | ● |
| OBS-01 |  | ● | ● |  |  |
| OBS-02 |  |  | ● | ● |  |
| OBS-03 |  |  | ● | ● |  |
| NFR-01 |  |  |  | ● |  |
| NFR-02 |  | ● |  |  |  |
| NFR-03 |  |  |  |  |  |
| NFR-04 | ● |  |  | ● | ● |
| NFR-05 |  | ● | ● |  |  |
| NFR-06 |  | ● |  |  |  |
| NFR-07 |  |  |  |  | ● |
| ODD-01 | ● |  |  |  |  |
| ODD-02 | ● | ● |  |  |  |
| ODD-03 |  | ● |  |  |  |
| ODD-04 |  | ● |  |  |  |
| ODD-05 |  | ● |  |  |  |
| ODD-06 | ● |  |  | ● |  |

## Changes from draft v0.1

- Rewritten in EARS with one *shall* each; the vague term *sufficient stopping distance* (T2) is replaced by the measurable amber rule AGT-03 (4.5 m/s²) together with AGT-02.
- ODD assumptions turned into verifiable requirements (ODD-01 … ODD-06). Daylight, dry road and visibility stay **assumptions**: the system cannot check or enforce them.
- Removed from the system requirements because they do not constrain `SmartIntersectionCore`: dashboard usability and display latency (NF-06, NF-09 → requirements of the dashboard), traceability (NF-12 → project rule), platform (NF-13 → project constraint), versioned schema (NF-11 → design decision in `protocol/`).
- Added: pause, single step and reset semantics (RUN-05 … RUN-07), separate ground truth (SV-02), dashboard loss (NFR-05).
