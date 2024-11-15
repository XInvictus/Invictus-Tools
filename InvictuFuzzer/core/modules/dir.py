import requests, threading, logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

class dir:
    def __init__(self, target: str, wordlist: str, threads: int) -> None:
        self.target = target
        self.wordlist = wordlist
        self.threads = threads
        self.progress = 0

        self.lock = threading.Lock()

        self.wordlist = self.load_wordlist()

        self.run()

    def load_wordlist(self) -> list:
        return [line.strip() for line in open(self.wordlist).readlines()]

    def check(self, file: str):
        try:
            name = "https://" + self.target + "/" + file
            r = requests.get(name)
            if r.status_code == 200:
                with self.lock:
                    log.info("[VALID] " + name)
        except Exception as e:
            pass

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.check, file_) for file_ in self.wordlist]
            for _ in as_completed(futures):
                pass