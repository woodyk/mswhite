"""
nl_rule_cli.py – Adds rules from natural descriptions.
Usage: python nl_rule_cli.py "If someone owns a thing, they influence it."
"""
import rule_naturalizer

def append_rule(nl_text):
    rule = rule_naturalizer.translate(nl_text)
    with open("rules.txt", "a") as f:
        f.write(rule + "\n")
    print("[OK] Added rule:", rule)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Provide a rule in natural language.")
    else:
        append_rule(" ".join(sys.argv[1:]))
