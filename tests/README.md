# Verification

Each test case is traced to at least one requirement in the Rhapsody `Requirements`
package. Write one file per test case using the template below; record each run in
`results/`.

## Template

```markdown
# TC-XX: <name>

| Field          | Value |
|----------------|-------|
| Requirement(s) | REQ-... |
| Scenario       | scenarios/sXX_....json |
| Preconditions  | ... |
| Action         | ... |
| Expected       | ... |
| Pass criterion | measurable, e.g. "vehicle stops ≥ 0 m before stop line" |
```

## Planned test cases (from the project plan)

| ID    | Name                     |
|-------|--------------------------|
| TC-01 | Red light compliance     |
| TC-02 | Green light operation    |
| TC-03 | Pedestrian protection    |
| TC-04 | Traffic phase safety     |
| TC-05 | Timing configuration     |
| TC-06 | V2X message handling     |
| TC-07 | Invalid configuration    |
