import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
HARNESS_STORE_DIR = BASE_DIR / ".harness_store"
VERSIONS_DIR = HARNESS_STORE_DIR / "versions"
TRACES_DIR = HARNESS_STORE_DIR / "traces"

# Ensure directories exist
HARNESS_STORE_DIR.mkdir(parents=True, exist_ok=True)
VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
TRACES_DIR.mkdir(parents=True, exist_ok=True)

# LLM Configs
DEFAULT_MODEL = "gpt-4o"
PROPOSER_MODEL = "gpt-4o"  # In the paper, proposer is Claude Code. We'll simulate with gpt-4o for the prototype.
MAX_TOKENS = 4096

# Evaluation Configs
MAX_TASKS_PER_EVAL = 3
EVAL_TIMEOUT_SECS = 120
