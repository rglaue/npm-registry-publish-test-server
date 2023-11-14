from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from http import HTTPStatus

PORT = 8077

class PackageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type = self.headers.get('content-type')
        boundary = None
        
        if content_type and 'boundary=' in content_type:
            boundary = content_type.split('boundary=')[-1].encode()

        if boundary:
            data = self.rfile.read(int(self.headers['Content-Length']))

            parts = data.split(b'--' + boundary)
            for part in parts:
                if b'filename=' in part:
                    header, content = part.split(b'\r\n\r\n', 1)
                    filename = header.split(b'filename=')[-1].strip(b'"').decode()

                    storage_path = os.path.join(os.path.dirname(__file__), 'stored_packages')
                    os.makedirs(storage_path, exist_ok=True)

                    with open(os.path.join(storage_path, filename), 'wb') as f:
                        f.write(content.strip(b'\r\n--'))

                    self.send_response(HTTPStatus.CREATED)
                    self.end_headers()
                    self.wfile.write(f"Package {filename} stored successfully".encode())
                    return

        self.send_response(HTTPStatus.BAD_REQUEST)
        self.end_headers()
        self.wfile.write("Invalid request".encode())

def run_server(server_class=HTTPServer, handler_class=PackageHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {PORT}...")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Server shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
