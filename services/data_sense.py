# services/data_sense.py
import os
import time
from datetime import datetime
from services.base import Service

class DataSense(Service):
    def on_start(self):
        self.watch_dir = self.config.get("watch_dir", "watch")
        self.poll_interval = float(self.config.get("poll_interval", 2))
        self.record_journal = bool(self.config.get("record_journal", True))
        os.makedirs(self.watch_dir, exist_ok=True)
        self.seen = set(f for f in os.listdir(self.watch_dir) if not f.startswith("."))
        self.log.info(f"watching={self.watch_dir} seen={len(self.seen)}")

    def run(self):
        files = [f for f in os.listdir(self.watch_dir) if not f.startswith(".")]
        new_files = [f for f in files if f not in self.seen]
        if new_files:
            ts = datetime.now().isoformat(timespec="seconds")
            for f in new_files:
                self.log.info(f"new file: {f}")
                self.seen.add(f)
                if self.record_journal:
                    self._journal(f, ts)
        time.sleep(self.poll_interval)

    def _journal(self, filename, ts):
        path = os.path.join("gigi", "journal")
        os.makedirs(path, exist_ok=True)
        name = f"entry_{ts.replace(':','-')}_data_sense.md"
        with open(os.path.join(path, name), "w") as out:
            out.write(
                f"# Gigi Journal – DataSense\n\n"
                f"**When:** {ts}\n"
                f"**Noticed:** `{filename}`\n\n"
                f"A new presence in the watch space. I remember it now."
            )
