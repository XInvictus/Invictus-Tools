import requests, threading, logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

class Fuzz:
    def __init__(self, target: str, wordlist: str, threads: int) -> None:
        self.target = target
        self.wordlist = wordlist
        self.threads = threads

        self.lock = threading.Lock()

        self.run()

    def load_wordlist(self):
        return [line.strip() for line in open(self.wordlist).readlines()]

    def check(self, item: str, i: int):
        try:
            name = "https://" + self.target.replace("{FUZZ}", item)
            r = requests.get(name)
            if r.status_code == 200:
                log.info("[VALID] {} ".format(i) + name)
        except Exception as e:
            pass

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.check, item, i) for i, item in enumerate(self.load_wordlist())]
            for _ in as_completed(futures):
                pass