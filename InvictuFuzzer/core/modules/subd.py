import socket, threading, logging
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

class subd:
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

    def check(self, subdomain: str):
        domain = f"{subdomain}.{self.target}"
        try:
            if socket.gethostbyname_ex(domain)[2]:
                with self.lock:
                    log.info("[VALID] " + domain)
        except Exception:
            pass

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.check, subdomain) for subdomain in self.wordlist]
            for _ in as_completed(futures):
                pass