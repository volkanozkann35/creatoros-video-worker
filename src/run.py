print("🚀 VIDEO GODMODE ACTIVE", flush=True)

import file_watcher
import threading

print("WORKER ALIVE", flush=True)

t = threading.Thread(target=file_watcher.start_watcher, daemon=True)
t.start()

while True:
    import time
    time.sleep(60)
