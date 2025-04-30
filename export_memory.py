import json
from datetime import datetime
memory = json.load(open("memory.json"))
ts = datetime.utcnow().isoformat().replace(":", "-")
out = f"export_memory_{ts}.json"
json.dump(memory, open(out, "w"), indent=2)
print("[OK] Exported to", out)
