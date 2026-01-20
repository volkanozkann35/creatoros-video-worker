import time

print("🚀 VIDEO GODMODE ACTIVE")
print("WORKER ALIVE")

try:
    import file_watcher
    print("file_watcher loaded")
except Exception as e:
    print("file_watcher failed:", e)

while True:
    time.sleep(60)
