# Rule Engine

## Syntax

```
IF (<triple>) AND (<triple>) THEN (<triple>)
```

Variables start with `?`

## Examples

```
IF (?X, type, person) AND (?X, projects, ?Y)
THEN (?Y, has_owner, ?X)
```

## Usage

Run inference:
```bash
python rule_cli.py run
```

Add a rule:
```bash
python rule_cli.py add-rule "IF (?X, likes, ?Y) THEN (?Y, admired_by, ?X)"
```
