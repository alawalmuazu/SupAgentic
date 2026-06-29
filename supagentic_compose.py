#!/usr/bin/env python3
"""
supagentic_compose.py

The core engine for "SupAgentic Compose".
This script parses a DAG (Directed Acyclic Graph) of AI tools expressed in a .yaml pipeline file,
topologically sorts the dependencies, and executes the nodes in sequence/parallel, bridging 
the stdout/stderr of one agent directly into the stdin or explicit variables of the next.

Usage: 
    python supagentic_compose.py <pipeline.yaml>
"""

import sys
import json
import logging
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not found. Installing locally...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml

logging.basicConfig(level=logging.INFO, format="%(asctime)s | ComposeEngine | %(message)s")

class ComposeEngine:
    def __init__(self, pipeline_path: str):
        self.pipeline_path = Path(pipeline_path)
        if not self.pipeline_path.exists():
            raise FileNotFoundError(f"Pipeline file not found: {self.pipeline_path}")
            
        with open(self.pipeline_path, 'r', encoding='utf-8') as f:
            self.manifest = yaml.safe_load(f)
            
        self.nodes = self.manifest.get('nodes', {})
        self.results = {}
        
    def _topological_sort(self):
        """Resolves the dependency graph and returns a valid execution order."""
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(node_name):
            if node_name in temp_mark:
                raise Exception(f"Cyclic dependency detected at node: {node_name}")
            if node_name not in visited:
                temp_mark.add(node_name)
                for dep in self.nodes[node_name].get('depends_on', []):
                    if dep not in self.nodes:
                        raise Exception(f"Node {node_name} depends on non-existent node: {dep}")
                    visit(dep)
                temp_mark.remove(node_name)
                visited.add(node_name)
                order.append(node_name)
                
        for node in self.nodes:
            if node not in visited:
                visit(node)
                
        return order
        
    def _resolve_template(self, template_str: str) -> str:
        """Resolves variables like ${recon_node.extracted_data} from previous node outputs."""
        if not isinstance(template_str, str):
            return template_str
            
        import re
        # Find ${node.field}
        matches = re.finditer(r"\$\{([^}]+)\}", template_str)
        result = template_str
        for match in matches:
            full_tag = match.group(0)
            inner = match.group(1).split('.')
            if len(inner) >= 2:
                node = inner[0]
                field = inner[1] # e.g. stdout, exacted_data
                if node in self.results:
                    resolved_val = self.results[node].get(field, "")
                    # For simplicity, if it's the exact string, replace the whole thing.
                    if result == full_tag:
                        return resolved_val
                    result = result.replace(full_tag, str(resolved_val))
        return result

    def execute_node(self, node_name: str):
        config = self.nodes[node_name]
        tool_name = config.get('tool')
        logging.info(f"🚀 Initializing Node: [{node_name}] | Tool: {tool_name}")
        
        # Resolve Input Mappings
        input_map = config.get('input_mapping', {})
        stdin_data = self._resolve_template(input_map.get('stdin', ''))
        env_vars = {k: self._resolve_template(v) for k, v in input_map.get('env', {}).items()}
        
        args = config.get('args', [])
        # Call supagentic CLI
        cli_path = self.pipeline_path.parent / "supagentic.py"
        cmd = [sys.executable, str(cli_path), "run", tool_name] + args
        
        logging.info(f"   Executing: {' '.join(cmd)}")
        if stdin_data:
            logging.info(f"   Injected STDIN stream: {len(str(stdin_data))} bytes")
            
        # Merge ENV variables securely
        import os
        run_env = os.environ.copy()
        for k, v in env_vars.items():
            run_env[k] = str(v)
            
        # Spawn Subprocess
        try:
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE if stdin_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=run_env
            )
            
            stdout, stderr = process.communicate(input=str(stdin_data) if stdin_data else None)
            
            # Extract logic
            extracted = None
            if 'extract' in config:
                ext_type = config['extract'].get('type')
                if ext_type == 'json':
                    try:
                        # Find the first valid JSON block in the stdout
                        import re
                        json_match = re.search(r'(\{.*\})', stdout, re.DOTALL)
                        if json_match:
                            parsed = json.loads(json_match.group(1))
                            keys = config['extract'].get('keys', [])
                            extracted = {k: parsed[k] for k in keys if k in parsed}
                        else:
                            extracted = stdout
                    except Exception as e:
                        logging.warning(f"Failed JSON extraction: {e}")
                        extracted = stdout
                
            self.results[node_name] = {
                "stdout": stdout,
                "stderr": stderr,
                "extracted_data": extracted or stdout,
                "exit_code": process.returncode
            }
            logging.info(f"✅ Node Finished: [{node_name}] | Exit: {process.returncode}")
            
            try:
                sys.path.append(str(self.pipeline_path.parent))
                import memory_bus
                memory_bus.init_db()
                memory_bus.store_memory(tool_name, f"Compose:{node_name}", self.results[node_name])
                logging.info(f"💾 Commited [{node_name}] stdout to Unified Memory Tissue.")
            except Exception as e:
                logging.warning(f"Memory Bus insertion failed: {e}")
                
        except Exception as e:
            logging.error(f"❌ Node Execution Failed: [{node_name}] | Error: {e}")
            raise e

    def run(self):
        logging.info(f"Starting Compose DAG for '{self.manifest.get('name', 'Pipeline')}'")
        order = self._topological_sort()
        logging.info(f"Execution Order: {' -> '.join(order)}")
        
        for node in order:
            self.execute_node(node)
            
        logging.info("🏁 Pipeline Execution Complete.")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python supagentic_compose.py <pipeline.yaml>")
        sys.exit(1)
        
    engine = ComposeEngine(sys.argv[1])
    engine.run()
