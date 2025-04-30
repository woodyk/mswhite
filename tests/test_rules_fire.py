import rule_engine, json, networkx as nx, os, tempfile, importlib

def test_rule_inference(tmp_path, monkeypatch):
    # build small graph file
    g = nx.Graph()
    g.add_edge("Alice", "ProjectX", label="projects")
    g.add_edge("Alice", "person", label="type")
    nx.write_gjson(g, tmp_path/"knowledge_graph.json")
    # copy rules
    (tmp_path/"rules.txt").write_text("IF (?X, type, person) AND (?X, projects, ?Y) THEN (?Y, has_owner, ?X)\n")
    monkeypatch.chdir(tmp_path)
    importlib.reload(rule_engine)
    rule_engine.run_engine()
    G2 = nx.read_gjson(tmp_path/"knowledge_graph.json")
    assert G2.has_edge("ProjectX", "Alice")
