from __future__ import annotations
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from logger import setup_logger
from config import WATCH_FOLDER
from orchestrator import process_video

log = setup_logger("watcher")

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".webm"}

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        p = Path(event.src_path)
        if p.suffix.lower() in VIDEO_EXTS:
            log.info(f"🎬 VIDEO YAKALANDI: {p}")
            process_video(p)

def start_watching():
    watch = Path(WATCH_FOLDER)
    if not watch.exists():
        raise RuntimeError(f"WATCH_FOLDER path does not exist: {watch}")

    log.info(f"👀 IZLENEN KLASOR: {watch}")

    observer = Observer()
    observer.schedule(Handler(), str(watch), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    finally:
        observer.stop()
        observer.join()
