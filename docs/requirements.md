# Requirements — draft v0.1

*Smart Intersection Simulation System · 2IN70 Group 7 · not yet shown on the project page*

> [!IMPORTANT]
> **Draft v0.1** derived from Milestone 1 (stakeholders, conflicts C1–C4, ODD and checks
> T1–T5). In Week 2 these will be refined and entered in the Rhapsody `Requirements`
> package, where each one is traced to model elements and test cases.
> Priority: **M** must · **S** should · **C** could.

## 1. Functional requirements

| ID | The system shall … | Source | Prio |
|---|---|---|---|
| **F-01** | control the vehicle signals of two mutually exclusive movement groups (N/S, E/W) in the sequence green → amber → all-red → other group green. | road authority, ODD | M |
| **F-02** | grant pedestrian walk permission on a crossing only while no conflicting vehicle movement has permission. | pedestrians, C2 | M |
| **F-03** | accept crossing requests from pedestrian agents and serve each request in the next phase in which that crossing can be released. | pedestrians | M |
| **F-04** | accept operator requests to change the green (per group), amber, all-red and pedestrian walk durations. | operator, C3 | M |
| **F-05** | reject timing requests outside the ODD ranges (green 5–60 s, amber 2–5 s, all-red 1–3 s, walk 5–30 s) and report the reason. | road authority, C3 | M |
| **F-06** | activate an accepted timing plan only at the next all-red state, never during green, amber or a pedestrian clearance interval. | road authority, C3 | M |
| **F-07** | update the position and speed of every vehicle agent each simulation step, within 0–8.5 m/s and modelled acceleration and braking limits. | ODD | M |
| **F-08** | make vehicle agents stop before the stop line on red, and on amber when stopping is feasible, and proceed on green when the path is clear. | drivers, occupants, C1 | M |
| **F-09** | move pedestrian agents across a crossing at 0.8–1.8 m/s, starting only with walk permission. | pedestrians, ODD | M |
| **F-10** | base the smart vehicle's stop / yield / proceed decision on its *observed* state of signals, vehicles and pedestrians, kept separate from the ground truth. | smart-vehicle developers, C4 | M |
| **F-11** | make the smart vehicle treat a missing or low-confidence signal observation as *not green*. | occupants, C4, T5 | S |
| **F-12** | load a scenario defining geometry, agents, arrivals, timing plan and random seed. | operator | M |
| **F-13** | support start, pause, single step and reset of a run. | operator | M |
| **F-14** | publish every step a snapshot with simulation time, active phase, signal states and the id, type, position, speed and state of every agent. | operator | M |
| **F-15** | acknowledge every operator command as accepted or rejected, with a reason when rejected. | operator, C3 | M |
| **F-16** | log time-stamped events: phase changes, commands, stops at stop lines, crossing requests and completions, safety-rule violations. | course team, authority | M |
| **F-17** | compute per run: waiting time per agent, queue length per arm and number of vehicle stops. | operator, authority | S |
| **F-18** | accept detection events (class, light state, confidence) from an external perception service through the perception interface. | smart-vehicle developers | C |

## 2. Non-functional requirements

| ID | Category | Requirement | Source | Prio |
|---|---|---|---|---|
| **NF-01** | Safety | At no simulation step shall conflicting movements (N/S and E/W vehicles, or a vehicle group and a conflicting pedestrian crossing) have permission at the same time. | pedestrians, authority, T1 | M |
| **NF-02** | Safety | A vehicle agent with sufficient stopping distance shall never cross its stop line during red. | occupants, authority, T2 | M |
| **NF-03** | Reproducibility | Running the same scenario with the same seed and timing plan shall produce an identical event log. | operator, course team, T4 | M |
| **NF-04** | Authority | All traffic decisions shall be made in the executable Rhapsody model; external components may change model state only through validated commands. | course team, C3 | M |
| **NF-05** | Timing | The model shall run with a fixed simulation step (proposed dt = 0.1 s) and publish state at ≥ 10 Hz in real-time mode. | operator | S |
| **NF-06** | Responsiveness | A state change in the model shall be visible in the dashboard within 200 ms. | operator | S |
| **NF-07** | Robustness | Closing, restarting or sending a malformed message from the dashboard shall not stop or corrupt the simulation. | course team | M |
| **NF-08** | Observability | During a run, the active states of the signal and agent state machines shall be visible through Rhapsody animation. | course team | M |
| **NF-09** | Usability | Every configuration control shall show its unit, accepted range, active vs pending value and any rejection reason. | operator | S |
| **NF-10** | Modifiability | The perception source (idealized ↔ ML) shall be replaceable without changing the smart vehicle's decision logic. | smart-vehicle developers, C4 | S |
| **NF-11** | Interoperability | All messages between the model and external tools shall follow a versioned, documented schema. | course team | S |
| **NF-12** | Traceability | Every requirement shall be traced to at least one model element and one test case. | course team | M |
| **NF-13** | Environment | The system shall run on a single Windows laptop with Rhapsody 9.0, the MSVC toolchain and Python 3, using only localhost communication. | course team | M |

## 3. Acceptance checks (from Milestone 1)

| ID | Check | Verifies |
|---|---|---|
| T1 | At no step are N/S and E/W vehicle signals green together, or a pedestrian walk permitted with a conflicting vehicle movement. | NF-01, F-02 |
| T2 | A vehicle approaching with sufficient stopping distance never crosses its stop line during red. | NF-02, F-08 |
| T3 | Invalid signal durations are rejected; a valid in-run change never interrupts an active clearance interval. | F-05, F-06 |
| T4 | Repeating a scenario with the same arrivals but a different green time gives recorded, comparable phase, queue and waiting-time traces. | NF-03, F-16, F-17 |
| T5 *(later)* | Missing or low-confidence perception is never interpreted as a confirmed green or a clear crossing. | F-10, F-11 |
