import logging, argparse, os
from core.modules import ftp, ssh

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

class Logger:
    def logger(func):
        def wrapper(*args, **kwargs):
            log.info(f"Running {func.__name__}")
            try:
                x = func(*args, **kwargs)
                log.info(f"Finished {func.__name__}")
                return x
            except Exception as e:
                log.error(e)
                return None
        return wrapper
    
class Main(Logger):
    def __init__(self):
        self.modes = {
            "ftp": ftp.FTP,
            "ssh": ssh.SSH
        }
        parser = argparse.ArgumentParser()

        parser.add_argument("-ho", "--host", help="Target IP / Url", type=str, required=True)
        parser.add_argument("-m", "--mode", help="Mode", type=str, required=True)
        parser.add_argument("-u", "--username", help="Username", type=str, required=True)
        parser.add_argument("-p", "--password", help="Password", type=str, required=True)
        parser.add_argument("-t", "--threads", help="Threads", type=int, default=100)

        args = parser.parse_args()

        self.host = args.host
        self.mode = args.mode
        self.username = args.username
        self.password = args.password
        self.threads = args.threads


    @Logger.logger
    def load_credentials(self, credential):
        if not os.path.isfile(credential):
            return [credential]
        return [x.strip() for x in open(credential, "r", errors='ignore').readlines()]

    @Logger.logger
    def main(self):
        if self.mode not in self.modes:
            return None
        username = self.load_credentials(self.username)
        password = self.load_credentials(self.password)
        log.info(f"Found {len(username)} usernames and {len(password)} passwords")
        mode = self.modes[self.mode](self.host, username, password, self.threads)
        mode.run()

        


if __name__ == "__main__":
    main = Main()
    main.main()
    
