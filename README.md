CCHS project map — v0.4

A floor-plan / tree view of what's currently happening at CCHS, backed by a git repo of YAML files (git-as-CMS — no database, no login, no admin panel).

Live structure: click a project pill in the tree, and it expands (description, link, images) and highlights on the floor plan at the same time. Multiple projects can be open at once. Tree groups by any two of Type / Recency / Zone, swappable via dropdown, nested as coloured bubbles.

What this is NOT
Not a WordPress plugin or Media Library asset — see "Hosting" below for why.
Not a database-backed app — there is no login, no write-API, no server-side state. Content changes happen by editing YAML and re-publishing.
Architecture
projects/            git repo — one YAML file per project (the actual content)
static/
  floorplan.svg       the CCHS floor plan (viewBox-corrected)
  images/              project photos, referenced by filename from YAML
index.html            the whole app — floor plan, tree, all JS/CSS inline
build_json.py         generates projects.json from projects/*.yaml
projects.json          generated snapshot — what index.html actually fetches
app.py                 optional: local Flask preview server (not used in hosting)

Static hosting, not a live backend. index.html fetches projects.json — a flat, pre-generated snapshot of every project — via a plain relative path. Nothing runs server-side in production; any static host (Bluehost File Manager, GitHub Pages, etc.) can serve it as-is.

Editing content

Each project is one YAML file in projects/. Fields:

name: string
x, y: pin position on the floor plan (document units, from the coordinate tool)
label_x, label_y: where the project's label sits (offset from the pin,
                   connected by a thin line)
type: fun | boring-necessary | security
recency: current | living-memory | eons-past
zone: main-space | cyberspace | ...          (any string; freeform)
date_built: YYYY-MM                           (optional; sorts leaves within
                                                a branch — undated sorts last)
status: active | complete | archived
owner: string
description: string
link: https://...                             (optional)
images: [file1.jpg, file2.jpg]                 (optional; files live in
                                                 static/images/)

Edit directly and commit — no admin panel, no login required to view the repo's history. git log on a file is the audit trail.

Finding coordinates

Run the app locally (python app.py, see below) and click anywhere on the floor plan — it prints the exact x, y in the console/on-page readout, in the same coordinate space the YAML fields use. Click twice per project: once for the pin, once for where you want its label to sit.

Local workflow
Edit or add a .yaml file in projects/
Regenerate the static snapshot:
python build_json.py
Preview it exactly as a static host would serve it:
python -m http.server 8000
then visit http://127.0.0.1:8000
Commit the YAML change and the regenerated projects.json together
Upload/push to hosting

app.py (python app.py, port 5050) is a separate, optional live-reload preview — it reads YAML directly on every request, no rebuild step needed. Handy for quick iteration; not used by the deployed static site.

Hosting (Bluehost)

Upload the folder as-is via cPanel → File Manager (or FTP) into public_html/, e.g. public_html/project-map/ → live at yoursite.com/project-map/.

Not the WordPress Media Library or page editor — the app is a folder of interrelated files (index.html expects projects.json and static/ sitting right next to it via relative paths). The Media Library re-files every upload into a date-stamped path (/wp-content/uploads/2026/08/...) with no relation to the app's structure, which breaks those relative references. File Manager/FTP preserves the folder exactly as built.

To surface it inside the main site: link to the hosted URL from a WordPress page, or embed via an <iframe src="https://yoursite.com/project-map/"> (a shortcode plugin like Advanced iFrame can tidy this up, but still requires the File Manager upload first — it doesn't replace it).

Tree & map interaction
Tree by [axis] then [axis] — pick any two of Type / Recency / Zone; the tree nests as bubbles, palest (root) to most saturated (leaf pill)
Click a pill → expands in place (description, link, images) and highlights yellow on the floor plan, simultaneously. Multiple pills can be open at once.
Click again → collapses and un-highlights
Branch headers (▾/▸) toggle collapse independently of pill state
Known limitations / not yet built
No write path for non-technical members — editing still means comfort with git. A form-based submission path was considered and deliberately deferred; git-literacy at CCHS was judged high enough to not need it for v1.
zone values are freeform strings — no validation against a fixed list, so a typo creates a silent new branch rather than erroring.
Multi-level nesting is fixed at two axes (primary/secondary); no three-deep nesting.
projects.json must be manually regenerated and re-uploaded after every content change — no auto-rebuild on push (a GitHub Action could add this later if the manual step becomes annoying).
