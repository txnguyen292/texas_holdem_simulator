from pathlib import Path

file_dir = Path(__file__).resolve().parent
base_dir = file_dir.parent.parent

class CONFIG:
    app = base_dir / "app"
    src = base_dir / "src"

if __name__ == "__main__":
    print(base_dir)