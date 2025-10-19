# services/base.py
import threading
import time
import logging
import os
from logging.handlers import RotatingFileHandler

class Service:
    """Minimal service interface: start/stop + internal loop via run()."""
    def __init__(self, name, config=None):
        self.name = name
        self.config = config or {}
        self._stop = threading.Event()
        self._thread = None
        self.status = "stopped"
        self.log = self._make_logger()

    def _make_logger(self):
        os.makedirs("logs", exist_ok=True)
        logger = logging.getLogger(f"svc.{self.name}")
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            h = RotatingFileHandler(f"logs/{self.name}.log", maxBytes=1_000_000, backupCount=5)
            fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            h.setFormatter(fmt)
            logger.addHandler(h)
        return logger

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._runner, daemon=True)
        self._thread.start()
        self.status = "running"
        self.log.info("started")

    def _runner(self):
        try:
            self.on_start()
            while not self._stop.is_set():
                self.run()
        except Exception as e:
            self.status = f"error: {e}"
            self.log.exception("service crashed")
        finally:
            try:
                self.on_stop()
            finally:
                self.status = "stopped"
                self.log.info("stopped")

    def stop(self, timeout=5):
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=timeout)

    # Hooks to override
    def on_start(self): pass
    def run(self): time.sleep(1)
    def on_stop(self): pass
