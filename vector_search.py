#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: vector_search.py
# Author: Wadih Khairallah
# Description: 
# Created: 2025-04-29 21:41:38
"""
vector_search.py - Semantic similarity search using embeddings.json
Usage: python vector_search.py "query"
"""

import os
import json, numpy as np, sys
from numpy.linalg import norm
import subprocess

EMB_FILE = "embeddings.json"

def embed_query(text):
    prompt = f"Generate a 10-dim numeric embedding (comma separated) for: {text}"
    resp = subprocess.check_output(["python","host_adapter.py", prompt], text=True)
    return np.array([float(x) for x in resp.strip().split(",")[:10]])

def main():
    if len(sys.argv)<2:
        print("Provide query text.")
        return
    query = sys.argv[1]
    if not os.path.exists(EMB_FILE):
        print("No embeddings. Run embed_graph.py first.")
        return
    emb = json.load(open(EMB_FILE))
    qvec = embed_query(query)
    best = None
    best_sim = -1
    for node, vec in emb.items():
        v = np.array(vec)
        sim = np.dot(qvec,v)/(norm(qvec)*norm(v)+1e-9)
        if sim>best_sim:
            best_sim=sim
            best=node
    print(f"Best match: {best} (cosine {best_sim:.2f})")

if __name__ == "__main__":
    main()
