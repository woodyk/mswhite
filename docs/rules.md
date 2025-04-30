# Rule Engine

## Manual Syntax

```
IF (<triple>) AND (<triple>) THEN (<triple>)
```

Example:
```
IF (?X, type, person) AND (?X, projects, ?Y)
THEN (?Y, has_owner, ?X)
```

## Authoring by Natural Language

```
python nl_rule_cli.py "If a person oversees a project, they are responsible for it."
```

→ Appends:
```
IF (?X, oversees, ?Y) THEN (?X, responsible_for, ?Y)
```

You can also preview:
```
python rule_naturalizer.py "If Alice supervises Bob, she is above him."
```
