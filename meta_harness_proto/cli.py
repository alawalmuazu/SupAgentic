import argparse
import sys
from meta_harness_proto.version_store import VersionStore
from meta_harness_proto.evaluator import Evaluator
from meta_harness_proto.failure_detector import FailureDetector
from meta_harness_proto.proposer import Proposer
from meta_harness_proto.config import DEFAULT_MODEL

def run_meta_loop(iterations: int, model: str):
    print(f"🚀 Starting Meta-Harness Optimization Loop ({iterations} iterations)")
    
    store = VersionStore()
    evaluator = Evaluator(model_name=model)
    proposer = Proposer(version_store=store)
    
    # Reset active harness to baseline
    store.activate_version("v0")
    
    current_version = "v0"
    
    for i in range(1, iterations + 1):
        print(f"\n======================================")
        print(f" ITERATION {i}/{iterations} | Active: {current_version}")
        print(f"======================================")
        
        # 1. EVALUATE
        eval_result = evaluator.run_evaluation(current_version)
        print(f"\n[Metrics] Success Rate: {eval_result['success_rate'] * 100:.1f}%\n")
        
        if eval_result['success_rate'] == 1.0:
            print("🎉 Perfect success rate! Optimization complete.")
            break
            
        # 2. DIAGNOSE
        print(f"[Failure Detector] Analyzing traces for {current_version}...")
        detector = FailureDetector(current_version)
        diagnosis = detector.get_failure_diagnosis()
        
        # 3. PROPOSE
        next_version = f"v{i}"
        print(f"\n[Proposer] Generating patches for {next_version}...")
        success = proposer.propose_next_version(current_version, next_version, diagnosis)
        
        # 4. ACTIVATE NEW VERSION
        if success:
            store.activate_version(next_version)
            current_version = next_version
            print(f"[Core] Harness updated to {current_version}.")
        else:
            print(f"[Core] Proposer failed to yield valid code. Retrying next iteration on current version.")
            
    print("\n🏁 Meta-Loop Completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SupAgentic Meta-Harness Loop")
    parser.add_argument("-i", "--iterations", type=int, default=3, help="Number of meta-loop iterations.")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="Model to use for the agent.")
    
    args = parser.parse_args()
    run_meta_loop(args.iterations, args.model)
