import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.config import WATCH_FOLDER
from src.orchestrator import handle_video


if not WATCH_FOLDER:
    raise RuntimeError("WATCH_FOLDER is None. .env not loaded correctly.")

WATCH_FOLDER = os.path.abspath(WATCH_FOLDER)


class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(".mp4"):
            print(f"🎥 New video detected: {event.src_path}")
            handle_video(event.src_path)


def start_watcher():
    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    print(f"👀 Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
