from datetime import datetime


class Logger:
    def info(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] {timestamp} - {message}")


logger = Logger()