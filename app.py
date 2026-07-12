import os
import yaml
from flask import Flask, jsonify, render_template

app = Flask(__name__)

PROJECTS_DIR = os.path.join(os.path.dirname(__file__), "projects")


def load_projects():
    """Walk the git repo of YAML files and parse each into a dict.

    This is read-only: Flask never writes back to the repo. Editing a
    project means editing/committing the YAML file directly.
    """
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/projects")
def api_projects():
    return jsonify(load_projects())


if __name__ == "__main__":
    app.run(debug=True, port=5050)
