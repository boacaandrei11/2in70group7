# C++ bridge

Hand-written C++ that connects the Rhapsody-generated application to the Python
visualization. Kept outside `model/` so Rhapsody code generation never overwrites it.

```
bridge/
├── include/        UdpLink.h, StateSerializer.h, CommandParser.h
├── src/            matching .cpp files
└── third_party/    nlohmann/json.hpp (single-header JSON library, MIT)
```

## Responsibilities

| Class             | Does | Does not |
|-------------------|------|----------|
| `UdpLink`         | Open/close Winsock UDP sockets, send datagrams, non-blocking receive | Interpret messages |
| `StateSerializer` | Turn model state into a `state` JSON message (see `protocol/`) | Decide anything |
| `CommandParser`   | Parse + schema-check incoming commands, hand them to the model as events | Apply commands — the model validates and applies |

The model calls into the bridge (e.g. a `SimulationController` publishes state every
tick). Incoming commands become Rhapsody events (`evSetTiming`, `evLoadScenario`, …)
so that the state machines decide what happens.

## Build

Compiled as part of the Rhapsody component (see `model/README.md`). Links against
`ws2_32.lib`.
