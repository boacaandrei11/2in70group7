# 0002 — Model package structure and execution approach

**Date:** 2026-11-16 · **Status:** package structure accepted; execution approach proposed
(to be confirmed by the proof of concept, issues #1 and #3)

## Context

The course template and hands-on sessions use five top-level SysML packages
(Requirements, UseCases, Behaviour, Structure, Verification), and the final report
will follow the course structure. The model must also execute in Rhapsody and drive
the Python dashboard repeatably (Architecture & Panel Spec, gates G1–G7).

## Decision

**Package structure** — the five course packages at the top level, subsystems as
sub-packages (see `model/README.md`). Supersedes the subsystem-based split in 0001.

**Execution approach (proposed)**

1. **Fixed-step simulation clock.** One `SimulationController` block owns time.
   A periodic timeout (e.g. `tm(100)`, dt = 0.1 s) drives each step: read pending
   commands → update signals and agents → publish one snapshot.
   `sim_time = steps × dt`. No extra threads.
2. **State lives in the model.** Agent positions/speeds are block attributes in
   metres, origin at the intersection centre (x east, y north). Python only
   converts to pixels.
3. **Narrow integration surface.** Only `TelemetryPort` (outbound) and `CommandPort`
   (inbound, polled each step, non-blocking) call the hand-written C++ in `bridge/`.
   Incoming commands become events consumed by the state machines.
4. **Commands are requests.** Timing changes are validated against the ODD ranges
   and applied at the next safe phase boundary; every command gets an ack.
5. **Commanded vs observed.** The signal controller's commanded indication and a
   smart vehicle's observed indication are separate attributes; missing or
   uncertain observations have explicitly defined behaviour.

## Consequences

- Runs are reproducible for a given scenario + seed (supports test T4 / gate G5).
- Animation in Rhapsody runs at real time; a "simulation speed" option would change dt
  or the timeout period, to be decided later.
- Open: whether V2I (signal phase and timing broadcast) is added to the scope.
