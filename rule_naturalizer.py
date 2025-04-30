"""
rule_naturalizer.py – Translates natural language into SOULPACK rule syntax using host_adapter.
"""
import subprocess

def translate(nl):
    prompt = f"Convert this into SOULPACK rule syntax:\n\"{nl}\""
    out = subprocess.check_output(["python", "host_adapter.py", prompt], text=True)
    return out.strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print('Usage: python rule_naturalizer.py "natural language rule"')
    else:
        print(translate(" ".join(sys.argv[1:])))
