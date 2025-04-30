import json, os
MEMORY = "memory.json"

def teach():
    memory = json.load(open(MEMORY))
    print("🧠 TEACHING MODE (type 'exit' to quit)")
    while True:
        try:
            line = input(">> ").strip()
            if not line or line.lower() == "exit": break
            parts = line.split(":", 1)
            if len(parts) != 2:
                print("⚠️ Format: Entity.key: value")
                continue
            path, val = parts[0].strip(), parts[1].strip()
            entity, key = path.split(".", 1)
            if entity not in memory: memory[entity] = {}
            memory[entity].setdefault(key, [])
            if isinstance(memory[entity][key], list):
                memory[entity][key].append(val)
            else:
                memory[entity][key] = [memory[entity][key], val]
        except Exception as e:
            print("⚠️", e)
    with open(MEMORY, "w") as f:
        json.dump(memory, f, indent=2)
    print("[OK] Memory updated.")

if __name__ == "__main__":
    teach()
