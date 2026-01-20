import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "auto_videos")
)

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.lower().endswith(".mp4"):
            print(f"🎬 VIDEO YAKALANDI: {event.src_path}", flush=True)

def start_watcher():
    if not os.path.exists(WATCH_FOLDER):
        raise RuntimeError(f"WATCH_FOLDER yok: {WATCH_FOLDER}")

    print(f"👀 IZLENEN KLASOR: {WATCH_FOLDER}", flush=True)

    observer = Observer()
    observer.schedule(VideoHandler(), WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
