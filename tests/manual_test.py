from dygo import render
from pathlib import Path


print(render(Path(__file__).parent / "test.json"))
