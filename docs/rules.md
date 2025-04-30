# Rule Engine

## Syntax

```
IF (<triple>) AND (<triple>) THEN (<triple>)
```

## Authoring by Natural Language

Example:
```bash
python nl_rule_cli.py "If a person manages a project, then they own it."
```

This adds:
```
IF (?X, manages, ?Y) AND (?X, type, person) THEN (?Y, has_owner, ?X)
```

You may also run the translator alone:
```bash
python rule_naturalizer.py "If A supervises B then A is superior to B."
```
