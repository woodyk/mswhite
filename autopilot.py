"""
autopilot.py - Background Scheduler for SOULPACK
"""

import yaml
import threading
import time
import subprocess

CONFIG = "autopilot.yaml"

def parse_interval(interval):
    if interval.endswith("m"):
        return int(interval[:-1]) * 60
    elif interval.endswith("h"):
        return int(interval[:-1]) * 3600
    elif interval.endswith("d"):
        return int(interval[:-1]) * 86400
    else:
        raise ValueError("Unknown interval format.")

def run_task(action, interval):
    def worker():
        while True:
            try:
                subprocess.Popen(action, shell=True)
            except Exception as e:
                print(f"[WARN] Task failure: {e}")
            time.sleep(interval)
    t = threading.Thread(target=worker, daemon=True)
    t.start()

def main():
    try:
        with open(CONFIG, 'r') as f:
            cfg = yaml.safe_load(f)
        for task in cfg.get("tasks", []):
            interval_sec = parse_interval(task["every"])
            print(f"[AUTOPILOT] Starting {task['id']} every {interval_sec}s")
            run_task(task["action"], interval_sec)
    except Exception as e:
        print(f"[WARN] Autopilot config error: {e}")

if __name__ == "__main__":
    main()
