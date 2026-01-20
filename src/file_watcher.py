import os
import time
import logging
from dotenv import load_dotenv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# .env yükle (local + Render uyumlu)
load_dotenv()

WATCH_FOLDER = os.getenv("WATCH_FOLDER")

if not WATCH_FOLDER:
    raise RuntimeError("WATCH_FOLDER is None. .env not loaded correctly.")

if not os.path.isdir(WATCH_FOLDER):
    raise RuntimeError(f"WATCH_FOLDER path does not exist: {WATCH_FOLDER}")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

class VideoHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        if not file_path.lower().endswith(".mp4"):
            return

        logging.info(f"🎬 Yeni video algılandı: {file_path}")

        try:
            # Şu an sadece logluyoruz
            # İleride buraya upload / queue / publish eklenir
            logging.info(f"✅ Video işleme hazır: {file_path}")
        except Exception as e:
            logging.error(f"❌ Video işleme hatası: {e}")


def start_watcher():
    logging.info(f"👀 WATCH FOLDER başlatılıyor: {WATCH_FOLDER}")

    event_handler = VideoHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# run.py tarafından import edildiğinde otomatik başlasın
start_watcher()
