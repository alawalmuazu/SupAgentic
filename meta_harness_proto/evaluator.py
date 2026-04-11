import subprocess
import os
import uuid
import tempfile
from .harness import AgentHarness
from .trace_logger import TraceLogger
from .config import EVAL_TIMEOUT_SECS

class MockEnvironment:
    """A safe, isolated temp directory to run shell commands within during evaluation."""
    def __init__(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.cwd = self.tmpdir.name
        
    def run_cmd(self, cmd: str):
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                cwd=self.cwd,
                capture_output=True, 
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 124, "", "Command timed out."
        except Exception as e:
            return 1, "", f"Error executing command: {e}"

    def cleanup(self):
        self.tmpdir.cleanup()


class Evaluator:
    def __init__(self, model_name: str):
        self.model = model_name
        
        # Define some basic tasks to evaluate the harness over
        self.tasks = [
            {
                "id": "write_hello",
                "instruction": "Write a python script called hello.py that prints 'Hello World'. Do not execute it, just write it.",
                "verify_cmd": "cat hello.py | grep 'Hello World'"
            },
            {
                "id": "count_files",
                "instruction": "Create three empty files: a.txt, b.txt, c.txt. Then write the total count of .txt files into count.txt.",
                "verify_cmd": "cat count.txt | grep '3'"
            }
        ]

    def run_evaluation(self, version_id: str):
        print(f"\n[Evaluator] Running eval on harness version {version_id}")
        run_results = []
        
        for task in self.tasks:
            run_id = f"eval_{task['id']}_{str(uuid.uuid4())[:8]}"
            logger = TraceLogger(run_id, version_id)
            env = MockEnvironment()
            
            harness = AgentHarness(model=self.model, logger=logger, env_runner=env)
            
            print(f"  -> Task: {task['instruction']}")
            try:
                completed = harness.run(task['instruction'])
                
                # Check actual success
                if completed:
                    code, stdout, _ = env.run_cmd(task['verify_cmd'])
                    is_success = (code == 0)
                    reason = "Success" if is_success else "Validation failed post-completion."
                else:
                    is_success = False
                    reason = "Max steps reached without task_complete."
                    
            except Exception as e:
                is_success = False
                reason = f"Crashed: {e}"
                
            summary = logger.finish(is_success, reason)
            env.cleanup()
            
            run_results.append(summary)
            print(f"  -> Result: {'✅' if is_success else '❌'} ({reason})")
            
        success_rate = sum(1 for r in run_results if r['success']) / len(run_results)
        return {"success_rate": success_rate, "runs": run_results}
