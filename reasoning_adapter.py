"""
reasoning_adapter.py - Combines graph context with LLM for enriched answers.
Usage: python reasoning_adapter.py "question"
"""

import subprocess, json, networkx as nx, sys, os

GRAPH_FILE = "knowledge_graph.json"

def neighborhood(term):
    if not os.path.exists(GRAPH_FILE):
        return ""
    G = nx.read_gjson(GRAPH_FILE)
    if term in G.nodes:
        neigh = list(G.neighbors(term))
        return f"Neighbors of {term}: {', '.join(neigh)}"
    return ""

def main():
    if len(sys.argv) < 2:
        print("Provide a question.")
        return
    question = sys.argv[1]
    context = neighborhood(question.split()[0])
    prompt = f"Context: {context}\nQuestion: {question}"
    answer = subprocess.check_output(["python","host_adapter.py", prompt], text=True)
    print(answer.strip())

if __name__ == "__main__":
    main()
