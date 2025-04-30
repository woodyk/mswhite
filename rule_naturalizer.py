"""
rule_naturalizer.py – Translates natural language into SOULPACK rule syntax using host_adapter.
"""
import subprocess, re

def translate(nl):
    prompt = f"Convert this into compact SOULPACK rule syntax only. Example: IF (?X, likes, ?Y) THEN (?Y, admired_by, ?X)\n\nNatural language: \"{nl}\"\nRule:"
    raw = subprocess.check_output(["python", "host_adapter.py", prompt], text=True)
    return normalize(raw)

def normalize(text):
    lines = text.strip().splitlines()
    for line in lines:
        if line.startswith("IF ") and "THEN" in line:
            return line.strip()
    return lines[0] if lines else "INVALID"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python rule_naturalizer.py "natural language rule"')
    else:
        print(translate(" ".join(sys.argv[1:])))
