import logging, argparse
from core.modules import dir, subd, tld, fuzz

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)


class Logger:
    def logger(func):
        def wrapper(*args, **kwargs):
            log.debug(f"Executing {func.__name__}")
            try:
                func(*args, **kwargs)
                log.success(f"Executed {func.__name__}")
            except Exception as e:
                log.error(e)
        return wrapper
    

class Main(Logger):
    def __init__(self):
        self.modes = {
            "dir": dir.dir,
            "subd": subd.subd,
            "tld": tld.tld,
            "fuzz": fuzz.Fuzz
        }

        parser = argparse.ArgumentParser()
        parser.add_argument("-ho", "--host", help="Target host to scan. eg. google.com")
        parser.add_argument("-m", "--mode", help="Mode to use")
        parser.add_argument("-w", "--wordlist", help="Wordlist to use")
        parser.add_argument("-t", "--threads", help="Number of threads", default=500, type=int)

        args = parser.parse_args()

        self.target   = args.host
        self.mode     = args.mode
        self.wordlist = args.wordlist
        self.threads  = args.threads

        if not any([self.target, self.mode, self.wordlist]):
            log.error("Missing required arguments")
            parser.print_help()
            exit(1)

    def format_target(self, target: str) -> str:
        domain = ""
        blacklist = ["https://", "http://"]
        for b in blacklist:
            domain = target.replace(b, "")
        return domain

    def main(self):
        if self.mode.lower() not in self.modes:
            log.error(f"Invalid mode {self.mode}")
            exit(1)
        if not self.target or not self.wordlist:
            log.error("Missing required arguments")
            exit(1)
        self.modes[self.mode.lower()](self.format_target(self.target), self.wordlist, self.threads)

if __name__ == "__main__":
    main = Main()
    main.main()