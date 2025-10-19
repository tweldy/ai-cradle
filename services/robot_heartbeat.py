# services/robot_heartbeat.py
import time
from datetime import datetime
from services.base import Service

class RobotHeartbeat(Service):
    """
    Placeholder 'motor/robot' service.
    Just emits a heartbeat so the core can supervise lifecycle.
    """
    def on_start(self):
        self.interval = float(self.config.get("interval", 3))
        self.log.info(f"robot heartbeat up, interval={self.interval}s")

    def run(self):
        ts = datetime.now().isoformat(timespec="seconds")
        self.log.info(f"heartbeat {ts}")
        time.sleep(self.interval)
