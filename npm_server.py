#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
from http import HTTPStatus
import json
import base64

PORT = 8077
DEBUG = False  # Set this to True to enable debug mode

class PackageHandler(BaseHTTPRequestHandler):
    def do_PUT(self):

        body_length = int(self.headers.get('Content-Length', 0))
        body_data = self.rfile.read(body_length).decode('utf-8')
        if DEBUG:
            # Dump the entire HTTP request if DEBUG is True
            self.dump_request(body_data)
        json_object = json.loads(body_data)
        jo_attachments = json_object.get('_attachments')
        package_name = list(jo_attachments.keys())[0]
        print(package_name)
        if self.handle_package(json_object, package_name) and self.handle_metadata(json_object, package_name):
            self.send_response(HTTPStatus.CREATED)
            self.end_headers()
            self.wfile.write(f"Package {package_name} stored successfully".encode())
            return

        self.send_response(HTTPStatus.BAD_REQUEST)
        self.end_headers()
        self.wfile.write("Invalid request".encode())

    def handle_package(self, body_data, filename):
        package_data = base64.b64decode(body_data['_attachments'][filename]['data'])
        storage_path = os.path.join(os.path.dirname(__file__), 'stored_packages')
        os.makedirs(storage_path, exist_ok=True)

        with open(os.path.join(storage_path, filename), 'wb') as f:
            f.write(package_data)

        return True

    def handle_metadata(self, body_data, filename):
        metadata = body_data.copy()
        attachments = metadata.pop('_attachments', None)
        metadata_filename = filename.replace('.tgz', '.json')

        storage_path = os.path.join(os.path.dirname(__file__), 'stored_packages')
        os.makedirs(storage_path, exist_ok=True)

        with open(os.path.join(storage_path, metadata_filename), 'w') as f:
            json.dump(metadata, f)

        return True

    def dump_request(self, body_data):
        """
        Dump the entire HTTP request, including headers and body, to stdout.
        """
        print("\n***** Dumping HTTP Request *****")
        print(f"Request method: {self.command}")
        print(f"Request path: {self.path}")
        print(f"Request headers:\n{self.headers}")
        print("Request body:")
        print(body_data)
        print("\n***** End of Dump *****")

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
