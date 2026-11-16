# Rhapsody model

Source of truth for all system behaviour. Rhapsody 9.0, C++ project, Microsoft
(Visual Studio) build environment.

## Expected contents

```
model/
├── SmartIntersection.rpyx        project file
└── SmartIntersection_rpy/        one unit file per package (+ components, profiles)
```

Create the project here: **File → New → Project**, location `model/`, name
`SmartIntersection`, type SysML (or the course template), language C++.

## Package structure (each package saved as a separate unit)

| Package          | Contents |
|------------------|----------|
| `Requirements`   | Stakeholder needs, system requirements, ODD |
| `Architecture`   | System context, BDDs, IBDs, interfaces, ports |
| `TrafficControl` | Traffic light / phase controller, timing config + validation |
| `Pedestrians`    | Pedestrian state machines, crossing requests |
| `Simulation`     | Simulation controller, scenario manager, clock |
| `Vehicles`       | Smart vehicle controller, kinematics, decision logic |
| `V2X`            | V2I / V2V messages and manager |
| `Verification`   | Test scenarios, traceability to requirements |

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
3. Model files are marked `binary` in `.gitattributes`, so git will not merge them.
   On conflict: keep one version (`git checkout --ours/--theirs <file>`), open in
   Rhapsody, redo the other change.
4. After pulling, open the project and check it loads without "unresolved
   element" warnings before continuing.
5. Commit the `.rpyx` together with the unit files it references.
