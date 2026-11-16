# 0001 — Repository structure and model version control

**Date:** 2026-11-16 · **Status:** accepted

## Context

Two-person team. The system is an IBM Rhapsody 9.0 model (C++), a hand-written C++
communication bridge and a Python visualization. Rhapsody model files do not merge
reliably, and Rhapsody regenerates C++ code on every build.

## Decision

- Monorepo with `model/`, `bridge/`, `protocol/`, `viz/`, `scenarios/`, `tools/`,
  `tests/`, `docs/`.
- Generated code and build output are not committed; components end in `Component`
  so their output folders are ignored.
- Each model package is a separate unit file with one owner at a time; model files
  are `binary` in `.gitattributes` so git never auto-merges them.
- The C++/Python message format is defined once in `protocol/`.
- The report stays in Overleaf; only submitted PDFs and diagram sources live here.

## Consequences

- Parallel work is possible on separate packages; same-package edits must be
  coordinated.
- A fresh clone must be built in Rhapsody before it runs.
- `mock_sim.py` lets the viz be developed independently, but it must never be part
  of the demonstration.
