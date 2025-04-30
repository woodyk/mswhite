import networkx as nx, re, os, json
import gjson

GRAPH_FILE = "knowledge_graph.json"
RULES_FILE = "rules.txt"
_var = re.compile(r"\?[A-Za-z]+")

def load_graph():
    return gjson.read(GRAPH_FILE) if os.path.exists(GRAPH_FILE) else nx.Graph()

def save_graph(G):
    gjson.write(G, GRAPH_FILE)

def parse_rule(line):
    ante, cons = line.split("THEN")
    antecedents = [t.strip(" ()") for t in ante.replace("IF", "").split("AND")]
    consequent = cons.strip(" ()\n ")
    return antecedents, consequent

def match_pattern(triple, pattern):
    s, r, o = triple
    ps, pr, po = pattern
    mapping = {}
    for a, b in zip((s, r, o), (ps, pr, po)):
        if b.startswith("?"): mapping[b] = a
        elif a != b: return None
    return mapping

def substitute(cons, mapping):
    s, r, o = cons
    return tuple(mapping.get(x, x) for x in (s, r, o))

def fire_rules(G, rules):
    added = 0
    facts = [(u, d.get("label", "related"), v) for u, v, d in G.edges(data=True)]
    for antecedents, consequent in rules:
        patterns = [tuple(a.split(", ")) for a in antecedents]
        cons = tuple(consequent.split(", "))
        for fact in facts:
            mapping = match_pattern(fact, patterns[0])
            if mapping is None: continue
            new_fact = substitute(cons, mapping)
            if not G.has_edge(new_fact[0], new_fact[2]):
                G.add_edge(new_fact[0], new_fact[2], label=new_fact[1], inferred=True)
                added += 1
    return added

def run_engine():
    if not os.path.exists(RULES_FILE):
        print("No rules.txt")
        return
    rules = []
    for line in open(RULES_FILE):
        line = line.strip()
        if not line or line.startswith("#"): continue
        rules.append(parse_rule(line))
    G = load_graph()
    total = 0
    while True:
        added = fire_rules(G, rules)
        total += added
        if added == 0: break
    save_graph(G)
    print(f"[ENGINE] {total} inferred.")
