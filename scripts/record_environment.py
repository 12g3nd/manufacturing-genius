"""Record resolved report dependencies without absolute editable-install paths."""
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
rows = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True).splitlines()
rows = [r for r in rows if not r.startswith(("-e ", "#", "manufacturing-genius"))]
rows = [r + '; sys_platform == "win32"' if r.lower().startswith(("pywinpty==", "pywin32==")) else r for r in rows]
(ROOT / "requirements-lock.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
environment = {"python": platform.python_version(), "platform": platform.platform(),
               "quarto": subprocess.check_output(["quarto", "--version"], text=True).strip(),
               "node": subprocess.check_output(["node", "--version"], text=True).strip()}
for name in ("numpy", "matplotlib", "jupyter", "ipykernel", "pip"):
    environment[name] = metadata.version(name)
(ROOT / "data/environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
print(json.dumps(environment, indent=2))
