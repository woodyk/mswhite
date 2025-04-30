"""
host_adapter.py - Bridge SOULPACK to OpenAI or Ollama runtimes
Usage: python host_adapter.py "your prompt"
"""

import yaml, os, sys, json, requests

CONFIG_PATH = "host_config.yaml"

def load_cfg():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def call_openai(prompt, cfg):
    import openai
    openai.api_key = os.getenv(cfg["api_key_env"])
    if not openai.api_key:
        raise RuntimeError("OpenAI API key not found in env.")
    chat = openai.chat.completions.create(
        model=cfg["model"],
        messages=[{"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

def call_ollama(prompt, cfg):
    url = cfg["base_url"].rstrip('/') + "/api/generate"
    payload = {"model": cfg["model"], "prompt": prompt}
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    return r.json().get("response", "")

def main():
    if len(sys.argv) < 2:
        print("Usage: python host_adapter.py \"your prompt\"")
        return
    prompt = sys.argv[1]
    cfg = load_cfg()
    if cfg["runtime"] == "openai":
        print(call_openai(prompt, cfg["openai"]))
    elif cfg["runtime"] == "ollama":
        print(call_ollama(prompt, cfg["ollama"]))
    else:
        print("Unsupported runtime.")

if __name__ == "__main__":
    main()
