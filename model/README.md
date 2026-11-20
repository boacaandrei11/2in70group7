# Rhapsody model

Source of truth for all system behaviour. Rhapsody 9.0, C++ project, Microsoft
(Visual Studio) build environment.

## Contents

```
model/
└── SmartIntersection/                 created by Rhapsody (File → New → Project, location model/)
    ├── SmartIntersection.rpyx         project file  ← open this
    └── SmartIntersection_rpy/         one unit file (.sbsx) per package + DefaultComponent.cmpx
```

Not committed (see `.gitignore`): the per-user workspace `SmartIntersection.rpwx`
(open diagrams, window layout), the empty `SmartIntersection.save` marker, generated
code and backups. Rhapsody recreates them.

## Package structure (course SysML structure, each package a separate unit)

The five top-level packages follow the 2IN70 course template / SYSMOD approach.
Sub-packages group the subsystems inside them.

Status as of Milestone 2: ✅ = in the model, 🔄 = defined in the repo, loaded with a script, ⏳ = planned.

```
SmartIntersection
├── Requirements
│   └── SystemRequirements      🔄 containment tree SIS_Requirements → FUN / NFR / ODD →
│                               groups → 27 EARS requirements, diagrams RD0–RD7.
│                               Load with tools/requirements/rhapsody_import.py
├── UseCases                    ✅ ConfigureScenario, RunIntersection, InspectTelemetry,
│   │                              ExecuteTestRun, SubmitPerceptionDetections («refine» → requirements)
│   ├── Actors                  ✅ ScenarioOperator, ScenarioTestHarness, MLPerceptionService
│   └── UseCaseDiagrams         ✅ SmartIntersectionUseCases (system boundary = SmartIntersectionCore)
├── Structure
│   ├── Context                 ✅ SmartIntersectionCore (SOI), external blocks, SystemContext BDD
│   │                              with information flows and items
│   ├── Signals                 ⏳ TrafficSignalController (+ its state machine)
│   ├── Agents                  ⏳ VehicleAgent, SmartVehicle, ConventionalVehicle, PedestrianAgent
│   ├── Simulation              ⏳ SimulationController, ScenarioManager, IntersectionGeometry
│   ├── Interfaces              ⏳ TelemetryPort, CommandPort, PerceptionPort, events, interface blocks
│   └── ValueTypes              ⏳ units and types (m, s, m/s, SignalIndication, ...)
├── Behaviour
│   ├── Activities              ⏳ decision logic, command validation, scenario initialisation
│   └── Interactions            ⏳ sequence diagrams (timing change, stop at red, crossing request)
└── Verification
    ├── TestCases               ⏳ TC-xx traced to requirements
    └── TestHarness             ⏳ test-driver blocks / scenarios used for verification
```

**State machines:** in Rhapsody a statechart is owned by its block, so it appears
under the block in `Structure`. `Behaviour` holds the activities and sequence
diagrams that describe behaviour across blocks.

**Code generation scope:** the component builds `Structure` only (plus anything
in `Verification/TestHarness` when running tests). `Requirements`, `UseCases` and
`Behaviour` are not code.

To make a package its own file: right-click the package → **Unit → Edit Unit** →
tick *Store in separate file*. Rhapsody does this by default for new packages in
most configurations; check once.

## Components and generated code

- Name every component with the suffix `Component` (e.g. `SimComponent`). The
  `.gitignore` excludes `model/**/*Component/` folders, which is where Rhapsody
  writes generated code and build output. Generated code is never committed.
- Configuration settings for the bridge (once `bridge/` has code):
  - **Settings → Include Path:** path to `bridge/include` and `bridge/third_party`
  - **Settings → Additional Sources / Libraries:** the `bridge/src/*.cpp` files and
    `ws2_32.lib` (Winsock, for UDP)
  - Relative paths are resolved from the configuration's output folder, so they
    will look like `..\..\..\bridge\include`. Check the path after the first build.

## Rules for working on the model in git

1. Close Rhapsody (or save all) before `git pull`, `checkout` or `merge`.
2. One person edits a package at a time. Tell the other member before you start.
3. Model files are marked `-merge` in `.gitattributes`, so git will not merge them.
   On conflict: keep one version (`git checkout --ours/--theirs <file>`), open in
   Rhapsody, redo the other change.
4. After pulling, open the project and check it loads without "unresolved
   element" warnings before continuing.
5. Commit the `.rpyx` together with the unit files it references.
