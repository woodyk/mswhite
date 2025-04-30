import rule_cli, tempfile, os, importlib
def test_add_rule(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path/'rules.txt').write_text('')
    rule_cli.add_rule("IF (?A, likes, ?B) THEN (?B, liked_by, ?A)")
    txt = (tmp_path/'rules.txt').read_text()
    assert "likes" in txt
