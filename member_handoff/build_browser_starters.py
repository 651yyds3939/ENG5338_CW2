"""Build portable notebook entry points and refresh the individual handoff ZIPs."""
from pathlib import Path
import zipfile
import nbformat as nbf

ROOT = Path(__file__).resolve().parent
DATA = ROOT.parent / "data/gas-turbine-emissions.csv"
MODELS = {2: (1, "random_forest"), 3: (2, "extra_trees"), 4: (3, "hist_gradient_boosting")}

for member, (model_number, model_name) in MODELS.items():
    script_name = f"member{member}_model{model_number}.py"
    archive_name = f"GAS4_member{member}_starter.zip"
    notebook_name = f"member{member}_model{model_number}.ipynb"
    model_code = (ROOT / script_name).read_text().split('if __name__ == "__main__":')[0].strip()
    notebook = nbf.v4.new_notebook(cells=[
        nbf.v4.new_markdown_cell(f"""# GAS4 — Member {member}: model {model_number}

**This notebook is the existing `{notebook_name}` supplied in your ZIP. Open and
edit this file directly. Do not create a new notebook, TXT or Markdown file.**

Portable experiment entry for Windows/macOS/Linux Jupyter and Python-backed cloud
notebooks such as Colab. The common protocol is maintained by Wenyi. Do not edit
the shared split, scoring or dataset. Use the assigned model and the shared experimental protocol.

**Local Jupyter:** extract your starter ZIP and open this notebook in that folder.
**Colab:** upload this notebook, then upload `{archive_name}` to the runtime's file
panel. Run the following setup cell; files are extracted using Python.

Choose this notebook OR the `.py` entry as your working experiment. If you edit
the notebook, return this notebook and its result folder, not an unchanged script.
Only the linear reference has been verified; this candidate has NOT RUN by default.
"""),
        nbf.v4.new_code_cell(f'''from pathlib import Path
import sys
import zipfile

WORKDIR = Path.cwd()
if (WORKDIR / "member_handoff/cw2_common.py").is_file():
    WORKDIR = WORKDIR / "member_handoff"
if not (WORKDIR / "cw2_common.py").is_file():
    archive = WORKDIR / "{archive_name}"
    assert archive.is_file(), "Upload your starter ZIP to the runtime file panel first."
    WORKDIR = WORKDIR / "gas4_member{member}_work"
    WORKDIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            target = (WORKDIR / item.filename).resolve()
            assert target.is_relative_to(WORKDIR.resolve()), "Invalid archive path."
            if not target.exists():  # Preserve files you have already edited.
                bundle.extract(item, WORKDIR)
DATA_PATH = WORKDIR / "gas-turbine-emissions.csv"
if not DATA_PATH.is_file():
    DATA_PATH = WORKDIR.parent / "data/gas-turbine-emissions.csv"
assert DATA_PATH.is_file(), "Course CSV not found."
if str(WORKDIR) not in sys.path:
    sys.path.insert(0, str(WORKDIR))
print("Working folder:", WORKDIR.name)
print("Python:", sys.version)
'''),
        nbf.v4.new_markdown_cell("""## Dependencies

The five computational packages may already be installed in your cloud runtime.
This cell records their actual versions. Exact versions used by Wenyi are in
`requirements.txt`. Use a separate environment locally if you need to install them.
In IPython, `%pip install -r /path/to/requirements.txt` installs into the current
kernel environment; restart the kernel/runtime afterwards if packages changed.
Different package versions can affect numerical results. Final comparisons are
reproduced in one agreed environment. Do not assume any browser viewer can execute
Python: an active Python kernel is required.
"""),
        nbf.v4.new_code_cell('''from importlib.metadata import version, PackageNotFoundError
for package in ["numpy", "pandas", "scipy", "scikit-learn", "threadpoolctl"]:
    try:
        print(package, version(package))
    except PackageNotFoundError:
        print(package, "MISSING: install dependencies before continuing")
'''),
        nbf.v4.new_markdown_cell("""## Your model and search grid

Edit this section only, and record the reason for each change. Keep the shared
protocol and seed. Keep your assigned model. If a new model needs
scaling, pass `scale=True` in the call below. Coordinate additional preprocessing
with Wenyi so that it is learned within each training fold.
"""),
        nbf.v4.new_code_cell(model_code),
        nbf.v4.new_markdown_cell("""## Run your assigned model

Set `RUN_EXPERIMENT = True` when ready. This tunes the candidate on development
folds only. It does not evaluate the final hold-out. Local timing is not a fair
cross-machine benchmark. Member 5 measures final comparative cost on one runtime.
"""),
        nbf.v4.new_code_cell(f'''RUN_EXPERIMENT = False
if RUN_EXPERIMENT:
    summary = run_experiment("{model_name}", ESTIMATOR, GRID,
        DATA_PATH, WORKDIR / "member{member}_results")
else:
    print("NOT RUN: set RUN_EXPERIMENT to True to train your assigned model.")
'''),
        nbf.v4.new_markdown_cell("""## Your analysis and contribution

**Write your analysis here, in this existing Markdown/text cell.** Double-click
this cell, replace the placeholders below with your own text, then press
`Shift + Enter` to render it. Save the notebook with your code, outputs and analysis.
This is a text cell, not a code cell.

- Name / student ID: pending.
- What you actually implemented or changed: pending.
- Why this model and these settings: pending.
- Training versus validation evidence: NOT RUN.
- Temporal limitations / parameter boundaries / next steps: pending.
- AI tools used and what for: pending.

Replace placeholders with your actual work and evidence. Do not invent results.
"""),
        nbf.v4.new_markdown_cell("""## Export results

After the experiment completes, run this cell and download the result ZIP from
the file panel. Also save/download this notebook with your edits and outputs.
Colab's runtime files are temporary, so export before leaving the runtime.
"""),
        nbf.v4.new_code_cell(f'''import shutil
result_dir = WORKDIR / "member{member}_results"
if RUN_EXPERIMENT and (result_dir / "summary.json").is_file():
    exported = shutil.make_archive(str(WORKDIR / "member{member}_results"),
                                   "zip", root_dir=result_dir)
    print("Download this file and your edited notebook:", Path(exported).name)
else:
    print("No completed experiment in this run; no result archive exported.")
'''),
    ])
    notebook.metadata["kernelspec"] = {"name": "python3", "language": "python", "display_name": "Python 3"}
    nbf.validate(notebook)
    nbf.write(notebook, ROOT / notebook_name)
    packages = ROOT / "packages"
    packages.mkdir(exist_ok=True)
    with zipfile.ZipFile(packages / archive_name, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in ["cw2_common.py", script_name, notebook_name, "requirements.txt"]:
            bundle.write(ROOT / name, arcname=name)
        if member == 2:
            bundle.write(ROOT / "member2_交接说明.md", arcname="交接说明.md")
            bundle.write(ROOT / "member2_README.md", arcname="README.md")
        else:
            bundle.write(ROOT / f"member{member}_README.md", arcname="README.md")
        bundle.write(DATA, arcname="gas-turbine-emissions.csv")
    print(f"Built {notebook_name} and refreshed {archive_name}")
