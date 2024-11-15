import socket, threading, argparse, logging
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.modules.utils.general import *

from core.modules.methods.portinfo import port_lookup
from core.modules.methods.checkbanner import grab_banner
from core.modules.methods.get_title import grab_title


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
        self.progress = 0
        self.results  = {}
        self.lock     = threading.Lock()

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-i", "--ip", help="Target IP", required=True, type=str)
        self.parser.add_argument("-e", "--end", help="End Port", required=True, type=int)
        self.parser.add_argument("-t", "--threads", help="Threads", default=500, type=int)

        self.parser.add_argument("-cs", "--clearscreen", help="Clear Screen", required=False, default=False, type=bool)
        self.parser.add_argument("-a", "--ascii", help="Ascii Art", required=False, default=False, type=bool)
        
        self.args = self.parser.parse_args()
        self.ip      = self.args.ip
        self.end     = int(self.args.end)
        self.threads = int(self.args.threads)

        if self.args.clearscreen:
            clear_screen()

        if self.args.ascii:
            ascii_art()

    def check(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            con = s.connect_ex((self.ip, port))
            if con == 0:
                lookup = port_lookup(port)
                self.results[port] = {}
                self.results[port]["port"] = port
                self.results[port]["service"] = lookup["service"]
                self.results[port]["protocols"] = lookup["protocols"]
                banner = grab_banner(self.ip, port)
                if banner == "No Banner":
                    banner = grab_title(self.ip, port)
                if banner == "No Title":
                    banner = "No banner or title"
                self.results[port]["banner"] = banner
        except Exception as e:
            pass
        finally:
            with self.lock:
                self.progress += 1
            s.close()
    @Logger.my_decorater
    def start(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = [executor.submit(self.check, i) for i in range(self.end)]
            for future in as_completed(futures):
                with self.lock:
                    completed = (self.progress / self.end) * 100
                if completed % 10 == 0:
                    log.info(f"Completed: {completed}%")
        print("\n")

    @Logger.my_decorater
    def main(self):
        log.info("Starting scan on %s", self.ip)
        self.start()
        nice_output(self.results)

if __name__ == "__main__":
    main = Main()
    main.main()
