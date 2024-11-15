import hashlib, threading, argparse, logging
from concurrent.futures import ThreadPoolExecutor
from core.modules.utils.general import *
from core.modules.utils.logging import *
from core.modules.hashing.ntlm import ntlm_hash

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)

class Logger:
    def my_decorater(func):
        def wrapper(*args, **kwargs):
            log.info("Started running %s", func.__name__)
            try:
                func(*args, **kwargs)
                log.info("Finished running %s", func.__name__)
            except Exception as e:
                log.error(e)
        return wrapper

class Main(Logger):
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.progress = 0
        self.passwords = []
        self.result = ""
        self.cracked = False
        self.methods = {
            "sha1": hashlib.sha1,
            "sha224": hashlib.sha224,
            "sha256": hashlib.sha256,
            "sha384": hashlib.sha384,
            "sha512": hashlib.sha512,
            "sha3_224": hashlib.sha3_224,
            "sha3_256": hashlib.sha3_256,
            "sha3_384": hashlib.sha3_384,
            "sha3_512": hashlib.sha3_512,
            "md5": hashlib.md5,
            "blake2b": hashlib.blake2b,
            "blake2s": hashlib.blake2s,
            "shake_128": hashlib.shake_128,
            "shake_256": hashlib.shake_256,
            "ntlm": ntlm_hash
        }

        parser = argparse.ArgumentParser()
        parser.add_argument("-t", "--hash", help="Hash to crack", required=True)
        parser.add_argument("-m", "--method", help="Hashing method", required=True)
        parser.add_argument("-l", "--list", help="Password list file", required=True)
        
        args = parser.parse_args()
        self.hash = args.hash
        self.method = args.method
        self.list = args.list

    def check(self, hash_value, password, func):
        hashed_password = func(password.encode()).hexdigest()
        if hashed_password == hash_value:
            log.info(f"Password found: {password}")
            self.result = password
            self.cracked = True
        with self.lock:
            self.progress += 1

    @Logger.my_decorater
    def load_passwords(self):
        try:
            with open(self.list, "r", errors="ignore") as f:
                self.passwords = [line.strip() for line in f]
            log.info(f"Loaded {len(self.passwords)} passwords")
        except FileNotFoundError:
            log.error("Password list file not found")
            raise
        finally:
            f.close()
    
    def verify_method(self, method):
        if method not in self.methods:
            log.error(f"Invalid method: {method}")
            return False
        return True
    @Logger.my_decorater
    def run_method(self, hash, method):
        func = self.methods.get(method)
        if func is None:
            log.error(f"Invalid method: {method}")
            return

        log.info(f"Starting {method} method with hash {hash}")
        total_passwords = len(self.passwords)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.check, hash, password, func) for password in self.passwords]
            for i, future in enumerate(futures, 1):
                log.debug(f"Checking password {i}/{total_passwords}\r")
                if self.cracked:
                    break
                if i % (total_passwords // 10) == 0:
                    log.info(f"Progress: {i / total_passwords * 100:.2f}%")
    @Logger.my_decorater
    def main(self):
        if not self.verify_method(self.method):
            exit(0)
        log.debug("Loading passwords...")
        self.load_passwords()
        self.run_method(self.hash, self.method)

if __name__ == "__main__":
    main = Main()
    main.main()
