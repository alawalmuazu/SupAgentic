import json
from openai import OpenAI
from .trace_logger import TraceLogger

SYSTEM_PROMPT = """
You are an autonomous AI agent running in an evaluation environment. 
Your goal is to solve the task described by the user.

You have access to the following tools:
1. execute_commands: Runs shell commands in the environment.
2. task_complete: Marks the task as finished.

Before taking action, you must use structured thought. Think about your analysis of the state, and your plan for the next commands.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "execute_commands",
            "description": "Call this to execute commands in the terminal with your analysis and plan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "analysis": {
                        "type": "string",
                        "description": "Analyze the current state based on the terminal output provided."
                    },
                    "plan": {
                        "type": "string",
                        "description": "Describe your plan for the next steps."
                    },
                    "commands": {
                        "type": "array",
                        "description": "List of shell commands to run.",
                        "items": {"type": "string"}
                    }
                },
                "required": ["analysis", "plan", "commands"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "task_complete",
            "description": "Call this when the task is fully complete and all requirements are met.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

class AgentHarness:
    def __init__(self, model: str, logger: TraceLogger, env_runner):
        self.model = model
        self.logger = logger
        self.env = env_runner
        self.client = OpenAI() # Assumes OPENAI_API_KEY is set in environment, or use openrouter/etc.
        
    def run(self, task_instruction: str, max_steps: int = 15):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Task: {task_instruction}"}
        ]
        
        self.logger.log_input(0, task_instruction)
        
        for step in range(1, max_steps + 1):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=TOOLS,
                temperature=0.0,
            )
            
            msg = response.choices[0].message
            messages.append(msg)
            
            if not msg.tool_calls:
                # No tools called, prompt the model to call a tool
                err = "Error: You must output a tool call (execute_commands or task_complete)."
                self.logger.log_tool_result(step, "system_error", err)
                messages.append({"role": "user", "content": err})
                continue
                
            for tc in msg.tool_calls:
                func_name = tc.function.name
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError:
                    args = {}
                    
                self.logger.log_tool_call(step, func_name, args)
                
                if func_name == "task_complete":
                    # In this baseline harness, we just exit on task_complete
                    # The Proposer might add a double-verification step here!
                    return True
                    
                elif func_name == "execute_commands":
                    commands = args.get("commands", [])
                    output_text = ""
                    for cmd in commands:
                        code, stdout, stderr = self.env.run_cmd(cmd)
                        output_text += f"$ {cmd}\n[exitcode: {code}]\n{stdout}\n{stderr}\n"
                    
                    self.logger.log_tool_result(step, func_name, output_text)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": output_text
                    })
                    
        return False # Max steps reached
