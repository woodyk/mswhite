import argparse, json, os, subprocess, datetime
import gjson

def load_memory():
    return json.load(open("memory.json"))

def save_memory(mem):
    with open("memory.json", "w") as f:
        json.dump(mem, f, indent=2)

def cmd_teach():
    mem = load_memory()
    print("🧠 TEACHING MODE — type 'exit' to quit")
    while True:
        line = input(">> ").strip()
        if line.lower() in {"exit", ""}:
            break
        if ":" not in line or "." not in line:
            print("⚠️ Use format: Entity.key: value")
            continue
        path, val = map(str.strip, line.split(":", 1))
        entity, key = path.split(".", 1)
        if entity not in mem:
            mem[entity] = {}
        mem[entity].setdefault(key, [])
        if isinstance(mem[entity][key], list):
            mem[entity][key].append(val)
        else:
            mem[entity][key] = [mem[entity][key], val]
    save_memory(mem)
    print("[✔] Memory updated.")

def cmd_qa(question):
    subprocess.run(["python", "retrieval_qa.py", question])

def cmd_export():
    mem = load_memory()
    ts = datetime.datetime.utcnow().isoformat().replace(":", "-")
    path = f"export_memory_{ts}.json"
    json.dump(mem, open(path, "w"), indent=2)
    print("[✔] Exported to", path)

def cmd_refresh():
    subprocess.run(["python", "knowledge_graph.py"])
    subprocess.run(["python", "rule_cli.py", "run"])
    subprocess.run(["python", "embed_graph.py"])

def cmd_rules_suggest():
    subprocess.run(["python", "rules_suggest.py"])

def dispatch():
    parser = argparse.ArgumentParser(prog="soulctl", description="SOULPACK Command Interface")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("teach", help="Teach new facts to memory")
    sub.add_parser("refresh", help="Rebuild graph + inference + embeddings")
    sub.add_parser("export", help="Export memory.json to versioned file")

    qa = sub.add_parser("qa", help="Ask a question")
    qa.add_argument("text", nargs="+", help="Your question")

    rules = sub.add_parser("rules", help="Rule-related operations")
    rules_sub = rules.add_subparsers(dest="subcmd")
    rules_sub.add_parser("suggest", help="Propose candidate rules from graph")

    args = parser.parse_args()
    if args.cmd == "teach": cmd_teach()
    elif args.cmd == "export": cmd_export()
    elif args.cmd == "refresh": cmd_refresh()
    elif args.cmd == "qa": cmd_qa(" ".join(args.text))
    elif args.cmd == "rules" and args.subcmd == "suggest": cmd_rules_suggest()
    else: parser.print_help()

if __name__ == "__main__":
    dispatch()
