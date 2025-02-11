from pathlib import Path

from dygo import render

print(render(Path(__file__).parent / "test.yaml"))
