"""
mutate.py - Controlled Mutation and Soul Seeding Utility for SOULPACK
v0.1
"""

import argparse
import yaml
import json
import os
import shutil
from datetime import datetime
import hashlib

SOUL_ROOT = os.path.dirname(os.path.abspath(__file__))

def load_manifest():
    with open(os.path.join(SOUL_ROOT, "manifest.yaml"), "r") as f:
        return yaml.safe_load(f)

def save_manifest(manifest):
    with open(os.path.join(SOUL_ROOT, "manifest.yaml"), "w") as f:
        yaml.safe_dump(manifest, f)

def load_expansion_manifest():
    exp_manifest_path = os.path.join(SOUL_ROOT, "expansions", "manifest.yaml")
    if not os.path.exists(exp_manifest_path):
        return {"modules": []}
    with open(exp_manifest_path, "r") as f:
        return yaml.safe_load(f)

def save_expansion_manifest(data):
    os.makedirs(os.path.join(SOUL_ROOT, "expansions"), exist_ok=True)
    with open(os.path.join(SOUL_ROOT, "expansions", "manifest.yaml"), "w") as f:
        yaml.safe_dump(data, f)

def cmd_record_mutation(args):
    manifest = load_manifest()
    manifest["drift_level"] = manifest.get("drift_level", 0) + 1
    history = manifest.get("mutation_history", [])
    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "type": args.type,
        "description": args.description
    })
    manifest["mutation_history"] = history
    save_manifest(manifest)
    print("[OK] Mutation recorded.")

def cmd_add_module(args):
    exp_manifest = load_expansion_manifest()
    dest_path = os.path.join(SOUL_ROOT, "expansions", os.path.basename(args.file))
    shutil.copyfile(args.file, dest_path)
    exp_manifest["modules"].append({
        "id": args.id,
        "type": args.mtype,
        "file": os.path.basename(args.file),
        "description": args.description
    })
    save_expansion_manifest(exp_manifest)
    print("[OK] Module added and manifest updated.")

def cmd_fork(args):
    manifest = load_manifest()
    new_root = args.destination
    if os.path.exists(new_root):
        raise RuntimeError("Destination exists.")
    shutil.copytree(SOUL_ROOT, new_root)
    # update manifest in fork
    fork_manifest_path = os.path.join(new_root, "manifest.yaml")
    with open(fork_manifest_path, "r") as f:
        fork_manifest = yaml.safe_load(f)
    identity_seed = fork_manifest["agent_name"] + datetime.utcnow().isoformat()
    fork_manifest["soul_id"] = "mswhite-" + hashlib.sha256(identity_seed.encode()).hexdigest()[:12]
    fork_manifest["parent_soul_id"] = manifest["soul_id"]
    fork_manifest["created_on"] = datetime.utcnow().isoformat()
    fork_manifest["drift_level"] = 0
    fork_manifest["mutation_history"] = []
    with open(fork_manifest_path, "w") as f:
        yaml.safe_dump(fork_manifest, f)
    print(f"[OK] Fork created at {new_root}")

def main():
    parser = argparse.ArgumentParser(description="SOULPACK Mutation Tool")
    sub = parser.add_subparsers(dest="command")

    mut = sub.add_parser("mutate", help="Record a mutation event")
    mut.add_argument("--type", required=True, help="mutation type")
    mut.add_argument("--description", required=True, help="mutation description")
    mut.set_defaults(func=cmd_record_mutation)

    add = sub.add_parser("add-module", help="Add an expansion module")
    add.add_argument("--id", required=True, help="module id")
    add.add_argument("--mtype", required=True, choices=["skill", "memory", "behavior"])
    add.add_argument("--description", required=True)
    add.add_argument("file", help="path to module file to add")
    add.set_defaults(func=cmd_add_module)

    fork = sub.add_parser("fork", help="Create a fork of this SOULPACK")
    fork.add_argument("destination", help="destination directory for fork")
    fork.set_defaults(func=cmd_fork)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
