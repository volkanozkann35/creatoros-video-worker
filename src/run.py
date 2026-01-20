from logger import setup_logger
import file_watcher

log = setup_logger("run")

print("🚀 VIDEO GODMODE ACTIVE")
print("WORKER ALIVE")

try:
    file_watcher.start_watching()
except Exception as e:
    log.exception(f"file_watcher crashed: {e}")
    raise
