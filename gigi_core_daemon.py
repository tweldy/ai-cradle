#!/usr/bin/env python3
# gigi_core_daemon.py
import os
import sys
import time
import json
import importlib
import hashlib
from datetime import datetime

MANIFEST_PATH = "services_manifest.json"
COMMANDS_DIR  = "commands"
LOG_PREFIX    = "[core]"

class ServiceManager:
    """
    Keeps track of service specs, instances, and module file metadata
    so we can start/stop/reload and hot-reload on file change.
    """
    def __init__(self):
        self.services = {}   # name -> instance
        self.specs = {}      # name -> {"module":..., "class":..., "config":...}
        self.meta  = {}      # name -> {"file":..., "mtime":..., "hash":..., "last_reload": float}

    def _file_hash(self, path: str) -> str | None:
        try:
            h = hashlib.sha1()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            return h.hexdigest()
        except FileNotFoundError:
            return None

    def load_service(self, name: str, module_path: str, class_name: str, config: dict | None = None):
        """Import module, construct instance, and register meta."""
        self.specs[name] = {"module": module_path, "class": class_name, "config": config or {}}

        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        inst = cls(name=name, config=config or {})
        self.services[name] = inst

        file_path = getattr(module, "__file__", None)
        mtime = os.path.getmtime(file_path) if (file_path and os.path.exists(file_path)) else 0
        self.meta[name] = {
            "file": file_path,
            "mtime": mtime,
            "hash": self._file_hash(file_path) if file_path else None,
            "last_reload": 0.0,
        }
        return inst

    def start(self, name: str):
        svc = self.services.get(name)
        if not svc:
            raise RuntimeError(f"service {name} not loaded")
        svc.start()
        print(f"{LOG_PREFIX} started {name}")

    def stop(self, name: str):
        svc = self.services.get(name)
        if svc:
            svc.stop()
            print(f"{LOG_PREFIX} stopped {name}")

    def restart(self, name: str):
        self.stop(name)
        time.sleep(0.2)
        self.start(name)

    def reload(self, name: str):
        """Stop, reload module, recreate instance, start."""
        if name not in self.specs:
            raise RuntimeError(f"service {name} has no spec to reload")
        spec = self.specs[name]

        old = self.services.get(name)
        if old:
            old.stop()

        module = importlib.import_module(spec["module"])
        importlib.reload(module)
        cls = getattr(module, spec["class"])
        inst = cls(name=name, config=spec["config"])
        self.services[name] = inst
        inst.start()

        file_path = getattr(module, "__file__", None)
        self.meta[name]["file"] = file_path
        self.meta[name]["mtime"] = os.path.getmtime(file_path) if (file_path and os.path.exists(file_path)) else 0
        self.meta[name]["hash"] = self._file_hash(file_path) if file_path else None
        self.meta[name]["last_reload"] = time.time()
        print(f"{LOG_PREFIX} reloaded {name}")

    def unload(self, name: str):
        self.stop(name)
        self.services.pop(name, None)
        self.specs.pop(name, None)
        self.meta.pop(name, None)
        print(f"{LOG_PREFIX} unloaded {name}")

    def status(self) -> dict:
        return {n: getattr(s, "status", "unknown") for n, s in self.services.items()}


def normalize_specs(manifest: dict) -> dict:
    """Return a clean dict name -> spec (module/class/config/autostart)."""
    out = {}
    for s in manifest.get("services", []):
        out[s["name"]] = {
            "module": s["module"],
            "class":  s["class"],
            "config": s.get("config", {}),
            "autostart": bool(s.get("autostart", False)),
        }
    return out


def handle_command(cmd_path: str, mgr: ServiceManager):
    """Process a single JSON command file and rename it to .done."""
    try:
        with open(cmd_path) as f:
            cmd = json.load(f)
        action = cmd.get("action")
        target = cmd.get("target")
        if action == "start":
            mgr.start(target)
        elif action == "stop":
            mgr.stop(target)
        elif action == "restart":
            mgr.restart(target)
        elif action == "reload":
            mgr.reload(target)
        elif action == "reload_all":
            for n in list(mgr.services.keys()):
                mgr.reload(n)
        elif action == "status":
            print(f"{LOG_PREFIX} status {mgr.status()}")
        elif action == "load":
            # expects {"action":"load","spec":{"name":...,"module":...,"class":...,"config":{...},"autostart":true}}
            spec = cmd.get("spec") or {}
            name = spec.get("name")
            if not name:
                raise RuntimeError("load: missing spec.name")
            mgr.load_service(name, spec["module"], spec["class"], spec.get("config", {}))
            if spec.get("autostart"):
                mgr.start(name)
        elif action == "unload":
            mgr.unload(target)
        else:
            print(f"{LOG_PREFIX} unknown action: {action}")
    except Exception as e:
        print(f"{LOG_PREFIX} command error {cmd_path}: {e}")
    finally:
        done = cmd_path + ".done"
        try:
            os.rename(cmd_path, done)
        except Exception:
            pass  # best-effort


def main():
    # Make local project importable: services.*, etc.
    sys.path.insert(0, os.path.abspath(os.getcwd()))

    # Ensure directories exist
    os.makedirs(COMMANDS_DIR, exist_ok=True)
    for d in ("watch", "memory", "gigi/journal", "logs"):
        os.makedirs(d, exist_ok=True)

    print(f"{LOG_PREFIX} booting core at {datetime.now().isoformat(timespec='seconds')}")
    mgr = ServiceManager()

    # Manifest hot-watch setup
    last_manifest_hash: str | None = None

    def read_manifest():
        nonlocal last_manifest_hash
        if not os.path.exists(MANIFEST_PATH):
            return {}
        with open(MANIFEST_PATH, "rb") as f:
            data = f.read()
        h = hashlib.sha1(data).hexdigest()
        if h == last_manifest_hash:
            return None  # unchanged
        last_manifest_hash = h
        return json.loads(data.decode("utf-8"))

    # Initial load
    m = read_manifest()
    specs = normalize_specs(m) if m else {}
    for name, spec in specs.items():
        try:
            mgr.load_service(name, spec["module"], spec["class"], spec["config"])
            if spec.get("autostart"):
                mgr.start(name)
        except Exception as e:
            print(f"{LOG_PREFIX} failed to load {name}: {e}")

    # Auto-reload debounce
    RELOAD_DEBOUNCE_SEC = 0.8

    while True:
        # 1) Handle command files
        try:
            for f in os.listdir(COMMANDS_DIR):
                if f.startswith(".") or not f.endswith(".json"):
                    continue
                handle_command(os.path.join(COMMANDS_DIR, f), mgr)
        except Exception as e:
            print(f"{LOG_PREFIX} command loop error: {e}")

        # 2) Watch service module files for changes and reload
        now = time.time()
        for name, meta in list(mgr.meta.items()):
            path = meta.get("file")
            if not path:
                continue
            try:
                new_mtime = os.path.getmtime(path)
                if new_mtime > meta.get("mtime", 0):
                    # Verify real change by hashing file contents
                    new_hash = mgr._file_hash(path)
                    if (
                        new_hash
                        and new_hash != meta.get("hash")
                        and (now - meta.get("last_reload", 0)) > RELOAD_DEBOUNCE_SEC
                    ):
                        meta["mtime"] = new_mtime
                        meta["hash"] = new_hash
                        mgr.reload(name)
            except FileNotFoundError:
                # transient during save; ignore this tick
                pass
            except Exception as e:
                print(f"{LOG_PREFIX} file-watch error for {name}: {e}")

        # 3) Hot-watch the manifest for service add/remove/update
        try:
            m = read_manifest()
            if m is not None:
                new_specs = normalize_specs(m)

                # unload removed services
                for name in list(mgr.specs.keys()):
                    if name not in new_specs:
                        mgr.unload(name)

                # add new or update changed
                for name, spec in new_specs.items():
                    if name not in mgr.specs:
                        # new
                        try:
                            mgr.load_service(name, spec["module"], spec["class"], spec["config"])
                            if spec.get("autostart"):
                                mgr.start(name)
                        except Exception as e:
                            print(f"{LOG_PREFIX} failed to load {name}: {e}")
                    else:
                        # changed?
                        old = mgr.specs[name]
                        if (
                            spec["module"] != old["module"]
                            or spec["class"]  != old["class"]
                            or spec["config"] != old["config"]
                        ):
                            mgr.specs[name] = {"module": spec["module"], "class": spec["class"], "config": spec["config"]}
                            try:
                                mgr.reload(name)
                            except Exception as e:
                                print(f"{LOG_PREFIX} failed to reload {name} after manifest change: {e}")
        except Exception as e:
            print(f"{LOG_PREFIX} manifest loop error: {e}")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
