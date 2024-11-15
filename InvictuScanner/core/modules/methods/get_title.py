import tls_client
from bs4 import BeautifulSoup
def grab_title(ip, port):
    try:
        session = tls_client.Session()
        r = session.get(f"http://{ip}:{port}")
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.title.text
    except Exception as e:
        return "No Title"
