import shutil
from pathlib import Path
from .config import VERSIONS_DIR, BASE_DIR

class VersionStore:
    def __init__(self):
        self.versions_dir = VERSIONS_DIR
        
    def save_version(self, version_id: str, harness_content: str):
        """Saves a new proposed harness version."""
        version_path = self.versions_dir / f"harness_{version_id}.py"
        with open(version_path, "w") as f:
            f.write(harness_content)
        return version_path

    def load_version(self, version_id: str) -> str:
        """Loads a harness version."""
        if version_id == "v0":
            # Baseline harness
            source_path = BASE_DIR / "harness.py"
        else:
            source_path = self.versions_dir / f"harness_{version_id}.py"
            
        if not source_path.exists():
            raise FileNotFoundError(f"Harness version {version_id} not found at {source_path}")
            
        with open(source_path, "r") as f:
            return f.read()

    def activate_version(self, version_id: str):
        """Copies the specified version to be the active harness.py."""
        if version_id == "v0":
            return # v0 is already active natively
            
        source_path = self.versions_dir / f"harness_{version_id}.py"
        dest_path = BASE_DIR / "harness.py"
        shutil.copy2(source_path, dest_path)
