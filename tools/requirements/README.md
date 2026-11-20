# Requirements tooling

| File | Purpose |
|---|---|
| `requirements.json` | **Single editable source** of the system requirements (text, rationale, source, priority, verification, refining use cases) and of the containment structure. |
| `render.py` | Checks every requirement (EARS template, one *shall*, no vague terms, valid priority / verification / use case) and regenerates [`docs/requirements.md`](../../docs/requirements.md). `--tex DIR` also writes the LaTeX tables for the report. |
| `rhapsody_import.py` | Loads the JSON into the open Rhapsody model: containment tree, «refine» links from the use cases, and the requirement diagrams. Idempotent — a re-run updates text and adds what is missing; it never deletes. |

Workflow: edit `requirements.json` → `python tools/requirements/render.py` → commit →
`rhapsody_import.py` (on a `model/` branch, after announcing that you edit the
`Requirements` and `UseCases` packages).

## 1. Load the requirements into Rhapsody

1. Pull, open `model/SmartIntersection/SmartIntersection.rpyx` in Rhapsody 9.0.
2. In a terminal (Rhapsody stays open):
   ```bat
   pip install pywin32
   python tools\requirements\rhapsody_import.py --dry-run
   python tools\requirements\rhapsody_import.py
   ```
3. Read the summary. Anything listed under *need manual work* is done by hand with §2.
4. Check in the browser: `Requirements › SystemRequirements` holds `SIS_Requirements`
   with 9 nested containers and 36 requirements; each use case shows its «refine»
   dependencies under *Dependencies*.

## 2. Manual fallback (same result, by hand)

1. Right-click `Requirements` → *Add New › Package* `SystemRequirements`.
2. Right-click it → *Add New › Requirement* `SIS_Requirements`; on that one add the
   containers `FUN_Functional`, `NFR_NonFunctional`, `ODD_OperationalDesignDomain`, and on
   `FUN_Functional` add `SIG_SignalControl`, `RUN_ScenarioAndRunControl`,
   `AGT_RoadUserBehaviour`, `SV_SmartVehicle`, `OBS_TelemetryAndEvaluation`.
   (Nesting a requirement inside another is SysML containment.)
3. Add each requirement inside its container with the **name** from the JSON
   (`SIG_01_PhaseSequence`, …). In *Features*: **Specification** = the EARS text,
   **ID** = `SIG-01`, **Description** = rationale / source / priority / verification.
4. «refine»: on a requirement diagram draw a *Refine* dependency **from the use case
   to the requirement** (the use case refines the requirement), or right-click the use
   case → *Add New › Relations › Dependency*, pick the requirement, then set the
   stereotype `refine`. The pairs are the *Refined by* column of
   [`docs/requirements.md`](../../docs/requirements.md).

## 3. Requirement diagrams

| Diagram | Content |
|---|---|
| `RD0_RequirementStructure` | `SIS_Requirements` and the 8 containers — the containment tree |
| `RD1_SignalControl` … `RD7_OperationalDesignDomain` | one container, its requirements (containment) and the use cases that refine them («refine») |

The script creates and auto-populates them. Then, per diagram:

1. *Layout › Arrange* (or move by hand): container on top, requirements in a row below,
   use cases at the bottom.
2. If containment is not drawn, add it with the **containment** (⊕) link of the diagram
   toolbar, from the container to each requirement.
3. To keep the boxes small: right-click a requirement → *Display Options* → show *Name*
   and *ID* only (the full text is in the report table).
4. Export each diagram as PNG (Rhapsody's diagram image export in the *File* menu;
   if your installation lacks it, a screenshot of the zoomed-to-fit diagram is fine)
   into `docs/diagrams/rhapsody/`, named after the diagram, e.g.
   `RD1_SignalControl.png`. Also export `SystemContext` and
   `SmartIntersectionUseCases` there. The report uses exactly these file names.

## 4. Model clean-up (from the Milestone 2 review)

- Delete the actor `UseCases › Actors › PythonDashboard`: it has no relations and is
  not on any diagram; the dashboard is the block `Structure › Context › PythonDashboard`.
- The test harness and the ML service exist twice — as blocks in `Context` (BDD) and as
  actors in `Actors` (use case diagram). Keep one element per external entity (open
  point, see the report).
- `SystemContextInterfaces` and `SmartIntersectionCore › CoreInterfaces` are empty IBDs:
  delete them or fill them in Week 5 (ports and interfaces).
