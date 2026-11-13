"""Execute the notebook with this script's interpreter, without a global kernel install."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
path = root / 'ENG5338_CW2_notebook_GAS4.ipynb'
notebook = nbformat.read(path, as_version=4)
manager = KernelManager(kernel_name='python3')
manager.kernel_spec.argv = [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}']
client = NotebookClient(notebook, km=manager, timeout=1800,
                        resources={'metadata': {'path': str(root)}})
try:
    client.execute()
finally:
    nbformat.write(notebook, path)
    if manager.has_kernel:
        manager.shutdown_kernel(now=True)
errors = [out for cell in notebook.cells if cell.cell_type == 'code'
          for out in cell.outputs if out.output_type == 'error']
assert not errors
audit = {'completed_at_utc': datetime.now(timezone.utc).isoformat(),
         'status':'success', 'error_outputs':len(errors),
         'code_cells':sum(c.cell_type=='code' for c in notebook.cells),
         'executed_code_cells':sum(c.cell_type=='code' and c.execution_count is not None for c in notebook.cells),
         'notebook_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
         'execution':'fresh kernel; common selected-configuration validation; submitted search and cost audit; original HGB plus revised Extra Trees assessment/cache verification; prior exposure disclosed'}
dest=root/'results/submission/notebook_execution.json'
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(audit,indent=2)+'\n')
print(f'Executed and saved {path.name}: {audit["executed_code_cells"]} code cells, zero errors.')
