"""Check requirements.json and render it to Markdown and LaTeX.

    python tools/requirements/render.py            # check + write docs/requirements.md
    python tools/requirements/render.py --tex DIR  # also write LaTeX tables into DIR

requirements.json is the single editable source of the requirement text.
rhapsody_import.py loads the same file into the Rhapsody model.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

# EARS templates (Mavin et al.). Each requirement must match the template of its pattern.
EARS = {
    "Ubiquitous": r"^The system shall ",
    "State-driven": r"^While [^,]+, the system shall ",
    "Event-driven": r"^When [^,]+(, [^,]+)*, the system shall ",
    "Unwanted behaviour": r"^If .+, then the system shall ",
    "Optional feature": r"^Where [^,]+, the system shall ",
    "Complex (state + event)": r"^While [^,]+, when [^,]+, the system shall ",
}
# Vague or non-verifiable terms (INCOSE Guide for Writing Requirements, R7/R8/R26...).
VAGUE = ["should", " will ", " may ", "must", "appropriate", "adequate", "sufficient", "user-friendly",
         "as possible", "etc", "and/or", "approximately", "fast", "quickly", "easy", "robust", "efficient",
         "if possible", "where possible", "normally", "typically", "support"]
PRIORITY = {"M": "Must", "S": "Should", "C": "Could"}
VERIFICATION = {"Test", "Analysis", "Inspection", "Demonstration"}


def load():
    return json.loads((HERE / "requirements.json").read_text(encoding="utf-8"))


def check(data):
    errors = []
    ucs = set(data["use_cases"])
    containers = {c["id"] for c in data["containers"]}
    ids = Counter(r["id"] for r in data["requirements"])
    names = Counter([r["name"] for r in data["requirements"]] + [c["name"] for c in data["containers"]])
    for k, n in list(ids.items()) + list(names.items()):
        if n > 1:
            errors.append(f"duplicate id/name {k}")
    for c in data["containers"]:
        if c["parent"] and c["parent"] not in containers:
            errors.append(f"{c['id']}: unknown parent {c['parent']}")
    for r in data["requirements"]:
        t = r["text"]
        if r["parent"] not in containers:
            errors.append(f"{r['id']}: unknown parent")
        if r["pattern"] not in EARS or not re.match(EARS[r["pattern"]], t):
            errors.append(f"{r['id']}: text does not match EARS '{r['pattern']}'")
        if t.count(" shall ") != 1:
            errors.append(f"{r['id']}: must contain exactly one 'shall'")
        if not t.endswith("."):
            errors.append(f"{r['id']}: must end with a full stop")
        low = f" {t.lower()} "
        for w in VAGUE:
            if w in low:
                errors.append(f"{r['id']}: vague term '{w.strip()}'")
        if r["priority"] not in PRIORITY:
            errors.append(f"{r['id']}: bad priority")
        if r["verification"] not in VERIFICATION:
            errors.append(f"{r['id']}: bad verification method")
        for u in r["refined_by"]:
            if u not in ucs:
                errors.append(f"{r['id']}: unknown use case {u}")
        if not r["rationale"].strip():
            errors.append(f"{r['id']}: missing rationale")
    for u in ucs:
        if data["use_cases"][u].get("deferred"):
            continue
        if not any(u in r["refined_by"] for r in data["requirements"]):
            errors.append(f"use case {u} refines no requirement")
    if not any(r["pattern"] == "Unwanted behaviour" for r in data["requirements"]):
        errors.append("no unwanted-behaviour requirement")
    return errors


def stats(data):
    reqs = data["requirements"]
    kinds = Counter(r["kind"] for r in reqs)
    return {
        "total": len(reqs),
        "kinds": kinds,
        "patterns": Counter(r["pattern"] for r in reqs),
        "priority": Counter(r["priority"] for r in reqs),
        "verification": Counter(r["verification"] for r in reqs),
    }


# ── Markdown ────────────────────────────────────────────────────────────────

def md_text(s):
    return s.replace("m/s^2", "m/s²").replace(" 5-60 s", " 5–60 s").replace(" 2-5 s", " 2–5 s") \
            .replace(" 1-3 s", " 1–3 s").replace(" 5-30 s", " 5–30 s").replace("T1-T4", "T1–T4")


def render_md(data):
    st = stats(data)
    uc = data["use_cases"]
    out = []
    out.append(f"# System requirements — v{data['version']}\n")
    out.append(f"*Smart Intersection Simulation System · 2IN70 Group 7 · {data['date']} · Milestone 2*\n")
    out.append("> [!NOTE]\n> Generated from [`tools/requirements/requirements.json`](../tools/requirements/requirements.json)"
               " by `tools/requirements/render.py` — edit the JSON, not this file. The same JSON is loaded into the"
               " Rhapsody `Requirements` package by `tools/requirements/rhapsody_import.py`.\n")
    out.append("## Conventions\n")
    out.append(f"- **Subject.** {data['subject_note']}")
    out.append("- **Syntax.** Every requirement follows one EARS template: *Ubiquitous* (The system shall …), "
               "*State-driven* (While …, the system shall …), *Event-driven* (When …, the system shall …), "
               "*Unwanted behaviour* (If …, then the system shall …), *Optional feature* (Where …, the system shall …) "
               "or *Complex* (While …, when …, the system shall …). Exactly one *shall* per requirement; no "
               "*should / will / may*; units are SI.")
    out.append("- **Priority (MoSCoW).** M = must, S = should, C = could.")
    out.append("- **Verification.** Test, Analysis, Inspection or Demonstration.")
    out.append("- **Source.** Stakeholder (Milestone 1, revised 16 Nov), check T1–T5 and conflict C1–C4 the requirement comes from.")
    out.append("- **Refined by.** Use cases that refine the requirement with «refine» in the Rhapsody model.")
    out.append("- **Singular.** Lists (snapshot content, logged events, run metrics) are defined once below, so each requirement states one thing.\n")
    out.append("### Definitions\n")
    out.append("| Term | Meaning |\n|---|---|")
    for t, m in data.get("definitions", []):
        out.append(f"| *{t}* | {m} |")
    out.append("")
    out.append(f"**{st['total']} requirements:** {st['kinds']['F']} functional, {st['kinds']['NF']} non-functional, "
               f"{st['kinds']['ODD']} ODD · {st['patterns']['Unwanted behaviour']} unwanted-behaviour · "
               f"{st['priority']['M']} M / {st['priority']['S']} S / {st['priority']['C']} C.\n")
    out.append("## Use cases\n")
    out.append("| ID | Use case | Primary actor | Actor's goal |\n|---|---|---|---|")
    for name, u in uc.items():
        out.append(f"| {u['id']} | {name} | {u['actor']} | {u['goal']} |")
    out.append("")
    containers = {c["id"]: c for c in data["containers"]}
    order = ["SIG", "RUN", "AGT", "SV", "OBS", "NFR", "ODD"]
    out.append("## Requirement structure (containment)\n")
    out.append("```")
    out.append("SIS  System requirements (SmartIntersectionCore)")
    tops = ["FUN", "NFR", "ODD"]
    for i, top in enumerate(tops):
        c = containers[top]
        last_top = i == len(tops) - 1
        branch, pad = ("└── ", "    ") if last_top else ("├── ", "│   ")
        ids = [r["id"] for r in data["requirements"] if r["parent"] == top]
        span = f"  ({ids[0]} … {ids[-1]})" if ids else ""
        out.append(f"{branch}{top:<4} {c['title']}{span}")
        groups = [x for x in data["containers"] if x["parent"] == top]
        for j, g in enumerate(groups):
            gids = [r["id"] for r in data["requirements"] if r["parent"] == g["id"]]
            gb = "└── " if j == len(groups) - 1 else "├── "
            out.append(f"{pad}{gb}{g['id']:<4} {g['title']}  ({gids[0]} … {gids[-1]})")
    out.append("```\n")
    for g in order:
        c = containers[g]
        out.append(f"## {g} — {c['title']}\n")
        out.append("| ID | EARS | Requirement | Rationale | Source | Prio | Verif. | Refined by |")
        out.append("|---|---|---|---|---|---|---|---|")
        for r in [x for x in data["requirements"] if x["parent"] == g]:
            ref = ", ".join(uc[u]["id"] for u in r["refined_by"]) or "— (system-wide)"
            out.append(f"| **{r['id']}** | {r['pattern']} | {md_text(r['text'])} | {md_text(r['rationale'])} | "
                       f"{r['source']} | {r['priority']} | {r['verification']} | {ref} |")
        out.append("")
    out.append("## Traceability: requirement ↔ use case («refine»)\n")
    names = list(uc)
    out.append("| Req. | " + " | ".join(uc[n]["id"] for n in names) + " |")
    out.append("|---|" + "---|" * len(names))
    for r in data["requirements"]:
        out.append(f"| {r['id']} | " + " | ".join("●" if n in r["refined_by"] else "" for n in names) + " |")
    out.append("")
    out.append("## Changes in v1.1 (after internal review)\n")
    out.append("- Fewer, sharper requirements (36 → 27); lists moved into the definitions so every requirement is singular.")
    out.append("- No numbers that are not in Milestone 1: speed limits, braking value, perception thresholds and step length removed. "
               "The only numbers left are the Milestone 1 ODD limits (agent counts, timing ranges).")
    out.append("- Design constraints are not system requirements: *all decisions inside the Rhapsody model*, *animated state "
               "machines*, *replaceable perception source*, platform and schema versioning are recorded as design decisions instead.")
    out.append("- The planned perception extension (UC5) gets requirements once it is designed.")
    out.append("")
    return "\n".join(out)


# ── LaTeX ───────────────────────────────────────────────────────────────────

def tex_escape(s):
    s = s.replace("\\", r"\textbackslash{}")
    for a, b in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("$", r"\$")]:
        s = s.replace(a, b)
    s = s.replace("m/s^2", r"m/s\textsuperscript{2}")
    s = re.sub(r"(\d) m/s", r"\1~m/s", s)
    s = re.sub(r"(\d) s\b", r"\1~s", s)
    s = re.sub(r"(\d)-(\d)", r"\1--\2", s)
    s = s.replace("T1-T4", "T1--T4")
    s = s.replace("N/S", "N/S").replace("E/W", "E/W")
    return s


KEYWORDS = [r"^(While)\b", r"^(When)\b", r"^(If)\b", r"^(Where)\b", r", (when)\b", r", (then)\b", r"\b(shall)\b"]


def tex_ears(s):
    s = tex_escape(s)
    for k in KEYWORDS:
        s = re.sub(k, lambda m: m.group(0).replace(m.group(1), r"\textbf{" + m.group(1) + "}"), s, count=1)
    return s


PATTERN_SHORT = {"Ubiquitous": "ubiquitous", "State-driven": "state", "Event-driven": "event",
                 "Unwanted behaviour": "unwanted", "Optional feature": "optional", "Complex (state + event)": "complex"}


def render_tex(data, outdir: Path):
    """Write req_table_rows.tex (rows for a 5-column longtable) and req_trace_matrix.tex.

    Needs only booktabs, longtable, array and graphicx in the preamble.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    uc = data["use_cases"]
    containers = {c["id"]: c for c in data["containers"]}
    rows = []
    for g in ["SIG", "RUN", "AGT", "SV", "OBS", "NFR", "ODD"]:
        kind = r" \emph{(functional)}" if containers[g]["parent"] == "FUN" else ""
        rows.append(r"\addlinespace[3pt]\multicolumn{5}{@{}l}{\textbf{" + g + " -- " + tex_escape(containers[g]["title"])
                    + "}" + kind + r"}\\*")
        rows.append(r"\midrule")
        for r in [x for x in data["requirements"] if x["parent"] == g]:
            rat = tex_escape(r["rationale"]) + r" \emph{[" + tex_escape(r["source"]) + "]}"
            idcell = r"\textbf{" + r["id"] + r"}\newline{\scriptsize\emph{" + PATTERN_SHORT[r["pattern"]] + "}}"
            rows.append(f"{idcell} & {tex_ears(r['text'])} & {rat} & {r['priority']} & {r['verification']}\\\\")
    defs = [r"\emph{" + tex_escape(t) + "} & " + tex_escape(m) + r"\\" for t, m in data.get("definitions", [])]
    (outdir / "req_definitions_rows.tex").write_text("\n".join(defs) + "\n", encoding="utf-8")
    (outdir / "req_table_rows.tex").write_text("\n".join(rows) + "\n", encoding="utf-8")

    names = list(uc)
    reqs = data["requirements"]
    half = (len(reqs) + 1) // 2

    def matrix(part):
        L = [r"\begin{tabular}[t]{@{}l" + "c" * len(names) + "@{}}", r"\toprule",
             "Req. & " + " & ".join(uc[n]["id"] for n in names) + r"\\", r"\midrule"]
        for r in part:
            L.append(r["id"] + " & " + " & ".join(r"$\bullet$" if n in r["refined_by"] else "" for n in names) + r"\\")
        L += [r"\bottomrule", r"\end{tabular}"]
        return "\n".join(L)
    (outdir / "req_trace_matrix.tex").write_text(matrix(reqs[:half]) + "\n\\hspace{2em}\n" + matrix(reqs[half:]) + "\n",
                                                 encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tex", type=Path)
    a = ap.parse_args()
    data = load()
    errs = check(data)
    if errs:
        print("\n".join("ERROR: " + e for e in errs))
        sys.exit(1)
    (ROOT / "docs" / "requirements.md").write_text(render_md(data), encoding="utf-8")
    st = stats(data)
    print(f"OK: {st['total']} requirements {dict(st['kinds'])} patterns {dict(st['patterns'])} "
          f"prio {dict(st['priority'])} verif {dict(st['verification'])}")
    if a.tex:
        render_tex(data, a.tex)
        print(f"LaTeX tables written to {a.tex}")


if __name__ == "__main__":
    main()
