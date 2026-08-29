"""
build_json.py

Converts the YAML files in projects/ into a single projects.json,
for static hosting (Bluehost, GitHub Pages, etc.) where nothing
can run Flask/Python on request.

Run this manually whenever project content changes, then re-upload
projects.json (and any changed files under static/) to the host.

    python build_json.py
"""

import os
import json
import yaml

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "projects")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "projects.json")


def load_projects():
    projects = []
    for filename in sorted(os.listdir(PROJECTS_DIR)):
        if not filename.endswith((".yaml", ".yml")):
            continue
        path = os.path.join(PROJECTS_DIR, filename)
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        if data:
            data["_file"] = filename
            projects.append(data)
    return projects


if __name__ == "__main__":
    projects = load_projects()
    with open(OUTPUT_FILE, "w") as f:
        json.dump(projects, f, indent=2)
    print(f"Wrote {len(projects)} projects to {OUTPUT_FILE}")