from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import webbrowser


HOST, PORT = "127.0.0.1", 8765
URL = f"http://{HOST}:{PORT}/"
ROOT = Path(__file__).resolve().parent


class BuildHandler(SimpleHTTPRequestHandler):
    def guess_type(self, path):
        if path.endswith(".br"):
            path = path[:-3]
        if path.endswith(".wasm"):
            return "application/wasm"
        return super().guess_type(path)

    def send_response(self, code, message=None):
        super().send_response(code, message)
        self.send_header("X-Web-Test", "TikhayaZavod")
        self.send_header("Cache-Control", "no-cache")
        if code == HTTPStatus.OK and urlsplit(self.path).path.endswith(".br"):
            self.send_header("Content-Encoding", "br")


def main():
    launch_browser = "--open" in sys.argv[1:]
    handler = partial(BuildHandler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer((HOST, PORT), handler)
    except OSError:
        try:
            with urlopen(Request(URL, method="HEAD"), timeout=2) as response:
                already_running = response.headers.get("X-Web-Test") == "TikhayaZavod"
        except OSError:
            already_running = False
        if not already_running:
            raise
        if launch_browser:
            webbrowser.open(URL)
        return

    with server:
        print(f"Game server: {URL}\nClose this window to stop the server.", flush=True)
        if launch_browser:
            webbrowser.open(URL)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
