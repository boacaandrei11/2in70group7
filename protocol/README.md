# Rhapsody ↔ Python protocol — draft v0.1

The contract between `bridge/` (C++) and `viz/` (Python). Change it here first,
then update both sides in the same pull request.

## Transport

| Item            | Value |
|-----------------|-------|
| Transport       | UDP over `127.0.0.1`, one JSON object per datagram, UTF-8 |
| State port      | `50010` — simulation → viz |
| Command port    | `50011` — viz → simulation |
| State rate      | 20 Hz target (one message per simulation tick or every N ticks) |
| Max size        | Keep messages < 8 KB (well under the UDP limit) |

UDP may drop messages. State messages are full snapshots, so a lost one is simply
replaced by the next. Commands are acknowledged with an `ack` message on the state
port; the viz retries a command once if no `ack` arrives within 500 ms.

## Conventions

- **Units:** metres, seconds, m/s, m/s², degrees.
- **World frame:** origin at the intersection centre, `x` east, `y` north.
  Heading 0° = east, counter-clockwise positive. The viz converts to pixels.
- **Time:** `sim_time` is simulation time owned by the model, not wall-clock time.
- **IDs:** integers, unique per entity type, never reused within a run.
- **Versioning:** every message has `"v": 1`. Bump on breaking change.
- **Enums:** upper-case strings (`"RED"`, `"APPROACHING"`).

## Messages

| `type`    | Direction | Schema |
|-----------|-----------|--------|
| `state`   | sim → viz | `state.schema.json` |
| `ack`     | sim → viz | `state.schema.json` |
| `command` | viz → sim | `command.schema.json` |

The model is free to reject any command (`ack.accepted = false` with a `reason`),
e.g. a green time below the safe minimum.

## Open points

- Exact tick rate and whether state is sent every tick.
- Fields for vehicle perception (believed vs actual light state) — sketched in
  `state.schema.json` as `perceived_light`.
- V2X message log in the state stream, or a separate event message type.
