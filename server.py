import threading
import webbrowser
import http.server

import psudo

FILE = 'visualize/release1.1/PseudoCode.html'
PORT = 8000


class TestHandler(http.server.SimpleHTTPRequestHandler):
    """The test example handler."""
    allow_reuse_address = True

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers['content-length'])
        data_string = self.rfile.read(length)
        print('\ninput: {}\n'.format(data_string))
        try:
            result = bytes(psudo.psudo(), 'UTF-8')
        except:
            result = 'error'
        print('\nresult: {}\n'.format(result))
        self.wfile.write(result)


def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    server_address = ("", PORT)
    server = http.server.HTTPServer(server_address, TestHandler)
    server.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()
