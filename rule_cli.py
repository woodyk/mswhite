"""
rule_cli.py  –  Manage and query rules.

Usage:
  python rule_cli.py add-rule "IF (?X, type, person) THEN (?X, category, human)"
  python rule_cli.py run
"""
import argparse, os
import rule_engine

def add_rule(text):
    with open("rules.txt","a") as f:
        f.write(text.strip()+"\n")
    print("[OK] rule appended.")

def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd")
    sub.add_parser("run")
    ar=sub.add_parser("add-rule")
    ar.add_argument("rule_text")
    args=p.parse_args()
    if args.cmd=="run":
        rule_engine.run_engine()
    elif args.cmd=="add-rule":
        add_rule(args.rule_text)
    else:
        p.print_help()

if __name__=="__main__":
    main()
