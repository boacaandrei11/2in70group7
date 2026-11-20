# 0003 — How system requirements are written, stored and traced

**Date:** 2026-11-20 · **Status:** accepted

## Context

Milestone 2 asks for more than ten system requirements in EARS, each with an id,
rationale, priority and verification method, grouped by containment in a requirement
diagram and linked to the use cases with «refine». The draft v0.1 (16 Nov) mixed system,
dashboard and project requirements and used non-verifiable terms (e.g. *sufficient
stopping distance*). The requirement text is needed in three places: the Rhapsody model,
`docs/requirements.md` and the Overleaf report.

## Options

- Type the requirements into Rhapsody by hand and copy them to the docs and the report —
  three copies that drift apart, and many fields of manual work.
- Keep one machine-readable source in the repo and generate the rest — one place to edit;
  needs a small script per target.

## Decision

1. **Single source.** `tools/requirements/requirements.json` holds all requirement data.
   `render.py` checks it and generates `docs/requirements.md` (and the report tables);
   `rhapsody_import.py` loads it into `Requirements::SystemRequirements` (idempotent).
2. **Subject and syntax.** *The system* = the block `SmartIntersectionCore`. Every
   requirement uses exactly one EARS template and one *shall*; *should / will / may* and
   vague terms (sufficient, appropriate, etc.) are not allowed; values carry SI units.
   `render.py` enforces this.
3. **Scope.** Only requirements on the SOI. Requirements on the dashboard (usability,
   display latency), project rules (traceability), the platform and design constraints
   (decisions inside the Rhapsody model, animation, replaceable perception) are kept out
   of this set; design constraints are recorded as decisions (0002). No numbers other
   than the Milestone 1 ODD limits; behaviour parameters (e.g. braking limit) are
   defined in the behaviour model. Lists are defined once as terms, so every requirement
   stays singular. Environmental ODD conditions (daylight, dry road) stay *assumptions*, because the
   system cannot check or enforce them.
4. **Ids and grouping.** `<GROUP>-NN`, groups SIG, RUN, AGT, SV, OBS (functional), NFR,
   ODD. Grouping is SysML containment (requirements nested in container requirements),
   not packages, so it is visible on the requirement diagram.
5. **Attributes.** Rationale, source (stakeholder, check T1–T5, conflict C1–C4),
   priority (MoSCoW) and verification method (Test / Analysis / Inspection /
   Demonstration) are stored in the requirement's description in Rhapsody.
6. **«refine» direction.** From the use case to the requirement (the use case refines the
   requirement), as in SysML and SYSMOD. Every requirement is refined by at least one
   use case. UC5 (perception, planned extension) gets requirements once it is designed.

## Consequences

- Requirement changes are made in the JSON and re-imported; edits made only in Rhapsody
  are overwritten on the next import.
- Test cases (Week 3) reference the ids; every requirement keeps its id once published.
- v1.1 (2026-11-20) reduced the set from 36 to 27 after review; the ids were renumbered
  once, before submission.
