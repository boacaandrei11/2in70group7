"""Load requirements.json into the open Rhapsody model (Rhapsody 9.0, Windows).

What it creates (and updates on a re-run; nothing is ever deleted):

    Requirements                         (existing top-level package)
    └── SystemRequirements               (package)
        ├── SIS_Requirements             (requirement, containment root)
        │   ├── FUN_Functional
        │   │   ├── SIG_SignalControl ── SIG_01_PhaseSequence, ...
        │   │   └── ...
        │   ├── NFR_NonFunctional ────── NFR_01_..., ...
        │   └── ODD_OperationalDesignDomain ── ODD_01_..., ...
        └── RD0_RequirementStructure, RD1_SignalControl, ...   (requirement diagrams)

    plus one «refine» dependency  UseCase ──► Requirement  for every entry in "refined_by".

Usage (Rhapsody open with SmartIntersection.rpyx loaded, nobody else editing the
Requirements or UseCases package):

    pip install pywin32
    python tools\\requirements\\rhapsody_import.py --dry-run      # prints the plan, needs no Rhapsody
    python tools\\requirements\\rhapsody_import.py                # writes into the model and saves
    python tools\\requirements\\rhapsody_import.py --no-diagrams  # elements and links only

If a step fails the script reports it and continues; the summary at the end lists
what has to be done by hand (see README.md in this folder).
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET_PACKAGE = "SystemRequirements"
DIAGRAMS = [
    ("RD0_RequirementStructure", None),
    ("RD1_SignalControl", "SIG"),
    ("RD2_ScenarioAndRunControl", "RUN"),
    ("RD3_RoadUserBehaviour", "AGT"),
    ("RD4_SmartVehicle", "SV"),
    ("RD5_TelemetryAndEvaluation", "OBS"),
    ("RD6_NonFunctional", "NFR"),
    ("RD7_OperationalDesignDomain", "ODD"),
]

problems = []


def log(msg):
    print(msg, flush=True)


def problem(msg):
    problems.append(msg)
    print("  !! " + msg, flush=True)


def description(r):
    return (f"Rationale: {r['rationale']}\n"
            f"Source: {r['source']}\n"
            f"Priority: {r['priority']}   Verification: {r['verification']}   EARS: {r['pattern']}")


# ── Rhapsody COM helpers ────────────────────────────────────────────────────

def items(coll):
    if coll is None:
        return []
    return [coll.Item(i) for i in range(1, coll.Count + 1)]


def connect():
    import win32com.client  # pywin32
    errors = []
    for how in ("GetActiveObject", "Dispatch"):
        for progid in ("Rhapsody2.Application", "Rhapsody.Application"):
            try:
                app = getattr(win32com.client, how)(progid)
                prj = app.activeProject()
                if prj is not None:
                    print(f"Connected via {how}('{progid}')")
                    return app
                errors.append(f"{how}('{progid}'): connected, but no project is open in that Rhapsody instance")
            except Exception as e:  # noqa: BLE001
                errors.append(f"{how}('{progid}'): {e}")
    print("Could not reach Rhapsody. Details:")
    for e in errors:
        print("  - " + e)
    sys.exit("Fixes: (1) start Rhapsody and the terminal with the SAME rights (both normal, or both 'Run as administrator'); "
             "(2) register Rhapsody's COM server once: admin terminal -> \"<Rhapsody folder>\\rhapsody.exe\" -regserver; "
             "(3) Python and Rhapsody must both be 64-bit (or both 32-bit).")


def find(owner, name, meta):
    try:
        return owner.findNestedElement(name, meta)
    except Exception:
        return None


def get_or_create(owner, meta, name):
    el = find(owner, name, meta)
    if el is not None:
        return el, False
    if meta == "Package":
        try:
            return owner.addNestedPackage(name), True
        except Exception:
            pass
    return owner.addNewAggr(meta, name), True


def set_requirement(el, rid, text, desc):
    for attr, value in (("specification", text), ("description", desc), ("requirementID", rid)):
        try:
            setattr(el, attr, value)
        except Exception as e:  # noqa: BLE001
            if attr == "requirementID":
                # Older API: keep the id visible in the description instead.
                try:
                    el.description = f"ID: {rid}\n{desc}"
                except Exception:
                    problem(f"{el.name}: could not set id/description ({e})")
            else:
                problem(f"{el.name}: could not set {attr} ({e})")


def has_refine(uc, req):
    try:
        for d in items(uc.dependencies):
            target = d.dependsOn
            if target is not None and target.GUID == req.GUID:
                return True
    except Exception:
        pass
    return False


def add_refine(uc, req):
    if has_refine(uc, req):
        return False
    dep = uc.addDependencyTo(req)
    for st in ("refine", "Refine"):
        try:
            dep.addStereotype(st, "Dependency")
            return True
        except Exception:
            continue
    problem(f"«refine» stereotype could not be applied to {uc.name} -> {req.name}; set it in the Features dialog")
    return True


def make_diagram(app, pkg, name, elements):
    if find(pkg, name, "ObjectModelDiagram") is not None:
        log(f"  = diagram {name} exists, left unchanged")
        return
    diag = None
    for how in ("addObjectModelDiagram", "addNewAggr"):
        try:
            diag = pkg.addObjectModelDiagram(name) if how == "addObjectModelDiagram" \
                else pkg.addNewAggr("ObjectModelDiagram", name)
            break
        except Exception:
            continue
    if diag is None:
        problem(f"diagram {name} could not be created; create a Requirement Diagram by hand")
        return
    try:
        diag = diag.changeTo("Requirement Diagram") or diag
    except Exception:
        problem(f"{name}: created as Object Model Diagram; change it with right-click > Change To > Requirement Diagram")
    try:
        coll = app.createNewCollection()
        for el in elements:
            coll.addItem(el)
        diag.populateDiagram(coll, "AllRelations", "among")
        log(f"  + diagram {name} ({len(elements)} elements)")
    except Exception as e:  # noqa: BLE001
        problem(f"{name}: could not auto-populate ({e}); drag the elements listed in README.md onto it")


# ── main ────────────────────────────────────────────────────────────────────

def plan(data):
    log(f"Package Requirements::{TARGET_PACKAGE}")
    for c in data["containers"]:
        log(f"  requirement {c['name']:<32} id={c['id']:<4} owner={c['parent'] or TARGET_PACKAGE}")
    for r in data["requirements"]:
        log(f"  requirement {r['name']:<32} id={r['id']:<7} owner={r['parent']}  refined_by={r['refined_by']}")
    n = sum(len(r["refined_by"]) for r in data["requirements"])
    log(f"{len(data['containers'])} containers, {len(data['requirements'])} requirements, {n} «refine» links, "
        f"{len(DIAGRAMS)} diagrams")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-diagrams", action="store_true")
    a = ap.parse_args()
    data = json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))
    if a.dry_run:
        plan(data)
        return

    app = connect()
    prj = app.activeProject()
    if prj is None:
        sys.exit("No project open in Rhapsody.")
    log(f"Project: {prj.name}")
    top = find(prj, "Requirements", "Package")
    if top is None:
        sys.exit("Top-level package 'Requirements' not found.")
    pkg, new = get_or_create(top, "Package", TARGET_PACKAGE)
    log(("+ " if new else "= ") + f"package Requirements::{TARGET_PACKAGE}")

    el = {}
    for c in data["containers"]:  # parents are listed before children
        owner = pkg if c["parent"] is None else el[c["parent"]]
        req, new = get_or_create(owner, "Requirement", c["name"])
        set_requirement(req, c["id"], c["text"], c.get("title", "Containment root of the system requirements"))
        el[c["id"]] = req
        log(("+ " if new else "= ") + c["name"])
    for r in data["requirements"]:
        req, new = get_or_create(el[r["parent"]], "Requirement", r["name"])
        set_requirement(req, r["id"], r["text"], description(r))
        el[r["id"]] = req
        log(("+ " if new else "= ") + r["name"])

    ucs = {}
    for name in data["use_cases"]:
        try:
            ucs[name] = prj.findNestedElementRecursive(name, "UseCase")
        except Exception:
            ucs[name] = None
        if ucs[name] is None:
            problem(f"use case {name} not found; its «refine» links are skipped")
    added = 0
    for r in data["requirements"]:
        for u in r["refined_by"]:
            if ucs.get(u) is not None:
                try:
                    added += add_refine(ucs[u], el[r["id"]])
                except Exception as e:  # noqa: BLE001
                    problem(f"«refine» {u} -> {r['id']} failed ({e})")
    log(f"+ {added} «refine» dependencies added")

    if not a.no_diagrams:
        for name, group in DIAGRAMS:
            if group is None:
                members = [el[c["id"]] for c in data["containers"]]
            else:
                reqs = [r for r in data["requirements"] if r["parent"] == group]
                uc_names = sorted({u for r in reqs for u in r["refined_by"]})
                members = [el[group]] + [el[r["id"]] for r in reqs] + [ucs[u] for u in uc_names if ucs[u] is not None]
            make_diagram(app, pkg, name, members)

    try:
        prj.save()
        log("Project saved.")
    except Exception as e:  # noqa: BLE001
        problem(f"save failed ({e}); save in Rhapsody with Ctrl+S")
    if problems:
        log(f"\n{len(problems)} step(s) need manual work:")
        for p in problems:
            log("  - " + p)
    else:
        log("\nDone without problems. Tidy the diagram layouts, then export them (see README.md).")


if __name__ == "__main__":
    main()
