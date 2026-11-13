"""Build the local group-review folder and ZIP from the current submission files."""
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'submission'
NAME = 'GAS4_Group_Review'
ARCHIVE = OUT / 'ENG5338_CW2_GAS4_for_group.zip'
FILES = [
    'ENG5338_CW2_report_GAS4.pdf',
    'ENG5338_CW2_presentation_GAS4.pdf',
    'ENG5338_CW2_notebook_GAS4.ipynb',
    'ENG5338_CW2_presentation_GAS4.pptx',
    'report_content.md', 'presentation_notes.md', 'viva_preparation.md',
    '先看这里.txt',
]


def main():
    for name in FILES + ['ENG5338_CW2_reproducibility_GAS4.zip']:
        assert (OUT / name).is_file(), f'Build the submission files first: {name}'
    with tempfile.TemporaryDirectory(prefix='.group_review_', dir=OUT) as temporary:
        stage = Path(temporary)
        folder = stage / NAME
        folder.mkdir()
        for name in FILES:
            shutil.copy2(OUT / name, folder / name)
        shutil.copy2(ROOT / 'docs/en/SUBMISSION_GUIDE.md', folder / 'SUBMISSION_GUIDE.md')
        with zipfile.ZipFile(OUT / 'ENG5338_CW2_reproducibility_GAS4.zip') as source:
            assert source.testzip() is None
            for item in source.infolist():
                path = PurePosixPath(item.filename)
                assert not path.is_absolute() and '..' not in path.parts
                assert path.parts[0] == 'ENG5338_CW2'
                assert not {'.git', '.local_private', '__pycache__'}.intersection(path.parts)
            source.extractall(folder)
        (folder / 'README_FIRST.txt').write_text('''GAS4 — group review package

Start with these three course files in this folder:
1. ENG5338_CW2_report_GAS4.pdf — full report draft.
2. ENG5338_CW2_presentation_GAS4.pdf — presentation draft.
3. ENG5338_CW2_notebook_GAS4.ipynb — executed main notebook and results.

Editable material:
- report_content.md — report text, opens in a text or Markdown editor.
- ENG5338_CW2_presentation_GAS4.pptx — editable slides.

Presentation preparation:
- presentation_notes.md — 10-minute speaking plan and notes.
- viva_preparation.md — questions and answers for rehearsal.

Complete project:
- ENG5338_CW2/ — code, data, results and document-generation scripts.
- To rerun, use the notebook inside ENG5338_CW2/ and keep that directory together.
- Install requirements.lock.txt in a Python environment, then run
  python run_notebook.py from ENG5338_CW2/.
- SUBMISSION_GUIDE.md provides the English submission guide.

Please check your model section, name, student ID and contribution details.
All five student IDs use seven digits. Contribution confirmation awaits the group.
The draft uses Extra Trees: validation MAE 0.7226 and coverage 81.76%;
2014–2015 assessment MAE 0.8011 and coverage 73.36%.

After group review, upload one group set of the three course files listed above.
''', encoding='utf-8')
        with zipfile.ZipFile(stage / ARCHIVE.name, 'w', zipfile.ZIP_DEFLATED) as output:
            for path in sorted(folder.rglob('*')):
                if path.is_file():
                    output.write(path, path.relative_to(stage))
        with zipfile.ZipFile(stage / ARCHIVE.name) as output:
            assert output.testzip() is None
            for name in FILES:
                assert output.read(f'{NAME}/{name}') == (OUT / name).read_bytes()
        destination = OUT / NAME
        if destination.exists():
            backup = ROOT / '.local_private/group_review_versions' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup.mkdir(parents=True)
            shutil.move(str(destination), backup / NAME)
            if ARCHIVE.exists():
                shutil.copy2(ARCHIVE, backup / ARCHIVE.name)
        shutil.move(str(folder), destination)
        (stage / ARCHIVE.name).replace(ARCHIVE)
    print(f'Built {NAME}/ and {ARCHIVE.name} ({ARCHIVE.stat().st_size / 1024**2:.2f} MiB).')


if __name__ == '__main__':
    main()
