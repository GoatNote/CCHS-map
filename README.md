# CCHS project map — v0.1 test

## What this is
A prototype: a floor-plan / tree-view toggle for CCHS projects, backed by
a git repo of YAML files (git-as-CMS — no database, no write API).
Flask reads the repo and serves it as JSON; the frontend renders it.

## Setup
    pip install flask pyyaml
    python app.py

Then visit http://127.0.0.1:5050

## Editing content
Each project is one YAML file in projects/. Edit directly and commit —
no admin panel, no login. Fields:

    name: string
    x, y: floor-plan coordinates (pixels)
    type: fun | boring-necessary | security
    recency: eons-past | living-memory | current
    specs: list, e.g. [design, analogue, reverse-engineering]
    status: active | complete | archived
    owner: string
    description: string

Refresh the page after committing to see changes (Flask reads the repo
fresh on each /api/projects request).

## Structure
    app.py              Flask app (read-only repo parser + routes)
    templates/index.html frontend (floor/tree toggle, group-by-tag dropdown)
    projects/            the git repo — one YAML file per project bubble

## Next steps (not yet built)
- Multi-level tree nesting (type -> recency -> specs)
- A form-based edit path for members who'd rather not touch git directly
- Sync mechanism if this moves off localhost (webhook -> git pull)
