import json
import time
from datetime import datetime
from pathlib import Path
from .config import TRACES_DIR

class TraceLogger:
    def __init__(self, run_id: str, version_id: str):
        self.run_id = run_id
        self.version_id = version_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.trace_dir = TRACES_DIR / f"{version_id}_{run_id}_{timestamp}"
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        
        self.trace_file = self.trace_dir / "execution_trace.jsonl"
        self.summary_file = self.trace_dir / "summary.json"
        
        self.start_time = time.time()
        self.steps = []
        self.success = False
        
    def log_input(self, step: int, prompt: str):
        self._write_event({"event": "input", "step": step, "content": prompt})

    def log_tool_call(self, step: int, tool_name: str, args: dict):
        self._write_event({"event": "tool_call", "step": step, "tool": tool_name, "args": args})

    def log_tool_result(self, step: int, tool_name: str, result: str):
        self._write_event({"event": "tool_result", "step": step, "tool": tool_name, "result": result})

    def finish(self, success: bool, reason: str):
        self.success = success
        duration = time.time() - self.start_time
        summary = {
            "run_id": self.run_id,
            "version_id": self.version_id,
            "duration_sec": round(duration, 2),
            "success": success,
            "reason": reason,
            "total_steps": len(self.steps)
        }
        with open(self.summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        return summary

    def _write_event(self, event_data: dict):
        event_data["timestamp"] = datetime.now().isoformat()
        self.steps.append(event_data)
        with open(self.trace_file, "a") as f:
            f.write(json.dumps(event_data) + "\n")
