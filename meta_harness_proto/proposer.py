import re
from openai import OpenAI
from .config import PROPOSER_MODEL

PROPOSER_SYSTEM_PROMPT = """
You are a Staff AI Harness Engineer. 
Your job is to optimize `harness.py`, which is the Python code used by an AI agent to solve tasks. 
You will be provided with:
1. The current `harness.py` code.
2. An execution trace of a recent failed run.

Your goal is to figure out WHY the agent failed based on the trace, and then propose a code patch to `harness.py` to fix it. 
Often, failures happen because:
- Tools are confusingly described.
- The system prompt doesn't force enough planning.
- The agent marks tasks complete before actually verifying them.

IMPORTANT: Output your proposed `harness.py` code ENTIRELY inside ```python ... ``` blocks. Do not omit any parts of the file, output the full new source code.
"""

class Proposer:
    def __init__(self, version_store):
        self.store = version_store
        self.client = OpenAI()

    def propose_next_version(self, current_version_id: str, new_version_id: str, diagnosis: str) -> bool:
        """
        Reads the failure diagnosis, generates a rewritten harness.py, and saves it.
        Returns True if successful, False otherwise.
        """
        if not diagnosis or "No failures detected" in diagnosis:
            print("  -> Proposer: No failures detected, skipping optimization.")
            return False
            
        current_code = self.store.load_version(current_version_id)
        
        prompt = f"==== CURRENT HARNESS.PY ====\n{current_code}\n\n"
        prompt += f"==== FAILURE DIAGNOSIS ====\n{diagnosis}\n\n"
        prompt += "Rewrite harness.py to fix this failure mode. Output the full file in a python code block."
        
        print(f"  -> Proposer thinking... (Model: {PROPOSER_MODEL})")
        
        response = self.client.chat.completions.create(
            model=PROPOSER_MODEL,
            messages=[
                {"role": "system", "content": PROPOSER_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        reply = response.choices[0].message.content
        
        # Extract python code block
        match = re.search(r"```python\n(.*?)\n```", reply, re.DOTALL)
        if match:
            new_code = match.group(1).strip()
            self.store.save_version(new_version_id, new_code)
            print("  -> Proposer: Generated and saved new harness code.")
            return True
        else:
            print("  -> Proposer Error: Could not extract python block from response.")
            return False
