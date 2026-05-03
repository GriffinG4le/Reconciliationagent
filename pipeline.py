import json
import os
import argparse
from nodes.ingest_sheet import run as ingest_sheet_run
from nodes.read_pdf import run as read_pdf_run
from nodes.reconcile import run as reconcile_run
from nodes.export_sheet import run as export_sheet_run

STATE_FILE = "pipeline_state.json"

NODES = [
    ("ingest_sheet", ingest_sheet_run),
    ("read_pdf", read_pdf_run),
    ("reconcile", reconcile_run),
    ("export_sheet", export_sheet_run)
]

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"completed_nodes": [], "data": {}}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def run_pipeline(resume=False):
    state = load_state() if resume else {"completed_nodes": [], "data": {}}
    
    for name, func in NODES:
        if name in state["completed_nodes"]:
            print(f"Skipping {name} (already completed)...")
            continue
            
        print(f"Running node: {name}...")
        try:
            state["data"] = func(state.get("data", {}))
            state["completed_nodes"].append(name)
            save_state(state)
            print(f"Node {name} completed successfully.\n")
        except Exception as e:
            print(f"Node {name} FAILED! Error: {e}")
            print(f"Fix the code and run with --resume to continue from {name}.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true", help="Resume from last failed node")
    parser.add_argument("--reset", action="store_true", help="Clear state and start fresh")
    args = parser.parse_args()
    
    if args.reset and os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("Pipeline state cleared.")
        
    run_pipeline(args.resume)
