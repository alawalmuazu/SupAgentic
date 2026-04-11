# Self-Optimizing Harness Prototype: Implementation Plan

The objective is to build a prototype "Meta-Harness" system for SupAgentic. This system will execute tasks, log extensive execution traces, evaluate success, and use a Proposer agent to iteratively patch and optimize the harness code based on failure analysis.

## User Review Required
> [!IMPORTANT]
> Please review the module structure and the meta-loop flow below. Does this align with how you want the prototype integrated into your SupAgentic toolkit? We'll be writing this as an independent, modular Python package in the workspace `c:\Users\OMEN\Documents\SupAgentic\meta_harness_proto\`.

## Proposed Changes

We will create a new directory: `c:\Users\OMEN\Documents\SupAgentic\meta_harness_proto\` and build the following architecture.

### [Core Infrastructure]
The backbone of the meta-loop.

#### [NEW] [meta_harness_proto/config.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/config.py)
- Defines paths for the workspace, the `.harness_store` (filesystem logs), and LLM configurations.

#### [NEW] [meta_harness_proto/version_store.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/version_store.py)
- Manages the saving of harness versions to a filesystem directory.
- Mimics the paper's Git-like tracking of proposed harness code and associated traces.

#### [NEW] [meta_harness_proto/trace_logger.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/trace_logger.py)
- Captures all structured LLM inputs, tool executions (commands), responses, and task durations.
- Writes traces to the filesystem in a structured JSON/text format that the Proposer can easily parse.

---

### [The Evaluated Harness]
The actual agent harness that gets modified by the meta-loop.

#### [NEW] [meta_harness_proto/harness.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/harness.py)
- The baseline harness. Includes the core system prompt, context management, and the `execute_commands` / `task_complete` tool schemas.
- This is the file that the `proposer.py` will actively modify via regex/diffs or rewriting.

#### [NEW] [meta_harness_proto/evaluator.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/evaluator.py)
- Provides a simulated environment or simple tasks (e.g., "Find all text files and count lines," "Write a python script that fetches an API") to evaluate the current `harness.py`.
- Computes a simple success score and passes traces to the logger.

---

### [The Meta-Loop (Optimization)]
The system that observes and patches the harness.

#### [NEW] [meta_harness_proto/failure_detector.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/failure_detector.py)
- Analyzes paths in `.harness_store`. Identifies which recent tasks failed or took too long.
- Prepares a "diagnosis package" for the Proposer.

#### [NEW] [meta_harness_proto/proposer.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/proposer.py)
- The agent that acts as the "Harness Engineer."
- Takes the diagnosis from `failure_detector.py`, reads `harness.py`, and proposes code updates (e.g., changing tool descriptions, adjusting wait durations, adding double-confirmation logic).

#### [NEW] [meta_harness_proto/cli.py](file:///c:/Users/OMEN/Documents/SupAgentic/meta_harness_proto/cli.py)
- The entry point. Runs the meta-loop: `Evaluate -> Log -> Detect Failures -> Propose Patch -> Update -> Repeat`.

## Verification Plan

### Automated Tests
- We will define a suite of 3 simple mock tasks in `evaluator.py`.
- We will run the meta-loop for 3 iterations to ensure the loop successfully modifies `harness.py`, logs the trace, and runs the next iteration without crashing.

### Manual Verification
- Review the generated traces in the `.harness_store` to confirm they contain the 10M-token style depth (raw context, not just summaries).
- Inspect the patches applied by the `proposer.py` to ensure they are logically sound improvements to `harness.py`.
