import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
import sys

class Watcher:
    def __init__(self, directory_to_watch):
        self.DIRECTORY_TO_WATCH = directory_to_watch
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        print(f"Watching directory: {self.DIRECTORY_TO_WATCH}")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        logging.basicConfig(filename="directory_watcher.log", level=logging.INFO)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            logging.info(f"{timestamp} - File created: {event.src_path}")

        elif event.event_type == 'modified':
            logging.info(f"{timestamp} - File modified: {event.src_path}")

        elif event.event_type == 'deleted':
            logging.info(f"{timestamp} - File deleted: {event.src_path}")

        elif event.event_type == 'moved':
            logging.info(f"{timestamp} - File moved: {event.src_path} to {event.dest_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <directory_to_watch>")
        sys.exit(1)

    path_to_watch = sys.argv[1]

    if not os.path.exists(path_to_watch):
        raise FileNotFoundError(f"The directory '{path_to_watch}' does not exist.")

    watcher = Watcher(path_to_watch)
    watcher.run()
