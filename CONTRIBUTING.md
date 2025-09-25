# Contributing

All textual or data changes follow a **Redline → PR → Review → Release** path.

**You must:**
1. Add a YAML header at the top of edited files:
```
---
module: act:t04_equivalence
locations: ["Title IV §4.2"]
dam_refs: ["DAM-003"]
ldai_refs: ["fig-ldai-07"]
change_type: MINOR
related_issue: 1234
risk: "no regression"
---
```
2. Tag each changed claim inline with `[[DAM:XXXX]]`.
3. Use branch naming `redline/<issue#>-<slug>`.

**Review**
- CI blocks PRs missing DAM tags or headers.
- See `docs/standards/review_checklist.md` for acceptance criteria.
