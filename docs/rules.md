# Rule Engine

## Syntax
```
IF (<triple>) AND (<triple>) THEN (<triple>)
Variables start with '?'
```

Example:
```
IF (?X, type, person) AND (?X, projects, ?Y)
THEN (?Y, has_owner, ?X)
```

Run inference:
```bash
python rule_cli.py run
```
Add a rule:
```bash
python rule_cli.py add-rule "IF (?A, likes, ?B) THEN (?B, respected_by, ?A)"
```
