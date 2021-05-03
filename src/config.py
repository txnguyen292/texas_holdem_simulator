from pathlib import Path

file_dir = Path(__file__).resolve().parent
base_dir = file_dir.parent

class CONFIG:
    app = base_dir / "app"
    reports = base_dir / "reports"

if __name__ == "__main__":
    pass