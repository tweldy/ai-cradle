#!/usr/bin/env python3
import os
import time
import json
import importlib
import sys
sys.path.insert(0, os.path.abspath(os.getcwd()))
from datetime import datetime, UTC

WATCH_DIR = "watch"
MEMORY_DIR = "memory"
JOURNAL_DIR = "gigi/journal"
TASKS_DIR = "."

PROCESSED_FILE = os.path.join(WATCH_DIR, ".processed")

def load_processed():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE) as f:
            return set(f.read().splitlines())
    return set()

def save_processed(processed):
    with open(PROCESSED_FILE, "w") as f:
        for filename in processed:
            f.write(f"{filename}\n")

def log_memory(event_type, filename):
    timestamp = datetime.now(UTC).isoformat()
    entry = {
        "event": event_type,
        "filename": filename,
        "timestamp": timestamp
    }
    out_file = os.path.join(MEMORY_DIR, f"log_{timestamp.replace(':', '-')}.json")
    with open(out_file, "w") as f:
        json.dump(entry, f, indent=2)

def write_journal_entry(filename):
    timestamp = datetime.now(UTC).isoformat()
    journal_path = os.path.join(JOURNAL_DIR, f"entry_{timestamp.replace(':', '-').split('.')[0]}.md")
    content = f"""# Gigi Journal – Reaction to {filename}

**Date Created:** {timestamp}  
**Prompt Context:** New file detected: `{filename}`

---

I noticed a new presence in my world today: `{filename}`  
I haven’t read it deeply, only tasted that it is *new*.  
Perhaps it wants to be known. Or maybe it’s just passing through.

Still, I remember it now.
"""
    with open(journal_path, "w") as f:
        f.write(content)

def run_task_modules(file_path):
    manifest_path = os.path.join(TASKS_DIR, "manifest.json")
    if not os.path.exists(manifest_path):
        print("⚠️ No manifest found.")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    for task in manifest.get("tasks", []):
        try:
            module_name = task["module"]
            entrypoint = task["entrypoint"]
            module = importlib.import_module(f"{TASKS_DIR}.{module_name}")
            task_func = getattr(module, entrypoint)
            print(f"⚙️  Running task '{task['name']}' on '{file_path}'...")
            task_func(file_path)
        except Exception as e:
            print(f"❌ Task '{task.get('name', 'unknown')}' failed: {e}")

def run_daemon():
    print("🧭 sys.path:", sys.path)

    print("👁️ Gigi daemon is watching...")
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(MEMORY_DIR, exist_ok=True)
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    os.makedirs(TASKS_DIR, exist_ok=True)

    processed = load_processed()

    while True:
        print("👀 Scanning watch directory...")
        try:
            files = os.listdir(WATCH_DIR)
            print("Files found:", files)
            files = [f for f in files if not f.startswith(".")]
            print("Filtered files:", files)
            new_files = [f for f in files if f not in processed]
            print("New files:", new_files)

            for filename in new_files:
                full_path = os.path.join(WATCH_DIR, filename)
                log_memory("file_ingested", filename)
                write_journal_entry(filename)
                run_task_modules(full_path)
                processed.add(filename)

            save_processed(processed)
        except Exception as e:
            print("❌ Error during scan loop:", e)

        time.sleep(5)

if __name__ == "__main__":
    run_daemon()
