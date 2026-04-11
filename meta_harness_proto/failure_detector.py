import json
from pathlib import Path
from .config import TRACES_DIR

class FailureDetector:
    def __init__(self, version_id: str):
        self.version_id = version_id
        
    def get_failure_diagnosis(self) -> str:
        """
        Scans traces for the given version, finds failures, 
        and extracts the exact execution trace for the proposer to analyze.
        """
        diagnosis_parts = []
        
        for trace_dir in TRACES_DIR.iterdir():
            if not trace_dir.is_dir() or not trace_dir.name.startswith(f"{self.version_id}_"):
                continue
                
            summary_file = trace_dir / "summary.json"
            trace_file = trace_dir / "execution_trace.jsonl"
            
            if not summary_file.exists() or not trace_file.exists():
                continue
                
            with open(summary_file, "r") as f:
                summary = json.load(f)
                
            if summary.get("success") == False:
                run_id = summary.get("run_id")
                reason = summary.get("reason")
                
                # Load the full trace
                trace_lines = []
                with open(trace_file, "r") as tf:
                    for line in tf:
                        trace_lines.append(json.loads(line))
                
                # Format a readable trace block
                trace_str = f"=== FAILURE TRACE: {run_id} ===\n"
                trace_str += f"Reason for failure: {reason}\n\n"
                
                for step_data in trace_lines:
                    event = step_data.get("event")
                    step_num = step_data.get("step")
                    if event == "input":
                        trace_str += f"[Step {step_num}] USER INSTRUCTION: {step_data.get('content')}\n"
                    elif event == "tool_call":
                        trace_str += f"[Step {step_num}] AGENT CALLED: {step_data.get('tool')}\nArgs: {json.dumps(step_data.get('args'))}\n"
                    elif event == "tool_result":
                        trace_str += f"[Step {step_num}] TOOL RESULT:\n{step_data.get('result')}\n"
                
                trace_str += "-" * 50 + "\n"
                diagnosis_parts.append(trace_str)
                
        if not diagnosis_parts:
            return "No failures detected for this version."
            
        return "\n".join(diagnosis_parts)
