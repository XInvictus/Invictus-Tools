import logging
import ftplib
from colorama import Back
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

class FTP:
    def __init__(self, host, username, password, threads=100):
        self.host = host
        self.username = username
        self.password = password
        self.threads = int(threads)

    def check(self, username, password):
        try:
            ftp = ftplib.FTP(self.host)
            ftp.login(username, password)
            log.info(f"{Back.MAGENTA}{username}:{password}{Back.RESET}")
        except:
            pass

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for username in self.username:
                for password in self.password:
                    futures.append(executor.submit(self.check, username, password))
            for _ in as_completed(futures):
                pass