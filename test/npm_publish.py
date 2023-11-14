#!/usr/bin/env python3

import requests
import sys
import os
import json
import base64

DEFAULT_PACKAGE = "calculator-1.0.0.tgz"
PORT = 8077

def create_body_data(package_path):
    with open(package_path, 'rb') as package_file:
        package_data = base64.b64encode(package_file.read()).decode('utf-8')

    body_data = {
        "_id": "no-package",
        "name": "no-package",
        "description": "no-package for testing npm_server.py",
        "dist-tags": {"latest": "1.0.0"},
        "versions": {
            "1.0.0": {
                "name": "no-package",
                "version": "1.0.0",
                "description": "no-package for testing npm_server.py",
                "main": "index.js",
                "publishConfig": {"registry": f"http://localhost:{PORT}"},
                "scripts": {"test": "echo \"Error: no test specified\" && exit 1"},
                "author": {"name": "Anonymous"},
                "license": "ISC",
                "_id": "no-package@1.0.0",
                "readme": "ERROR: No README data found!",
                "gitHead": "db91850381e4a5c3c0ac588a8cfeeafe98299fb6",
                "_nodeVersion": "20.8.0",
                "_npmVersion": "10.1.0",
                "dist": {
                    "integrity": "sha512-jFvssjrqh8dO8GwbJ5SGRFbKcoRDgnVF6b/hV0lrtkVvRrcYjHZLy5gGosV5kHuuMYT9jPSTehfqMOdJ9vwxYZ==",
                    "shasum": "df77e9798cbdb20e27ff3cec6baa75c09399999x",
                    "tarball": f"http://localhost:{PORT}/no-package/-/no-package-1.0.0.tgz",
                },
            }
        },
        "access": None,
        "_attachments": {
            f"{os.path.basename(package_path)}": {
                "content_type": "application/octet-stream",
                "data": package_data,
                "length": len(package_data),
            }
        },
    }

    return json.dumps(body_data)

def test_npm_server_package(package_path=None):
    package_to_publish = package_path if package_path else DEFAULT_PACKAGE

    if not os.path.exists(package_to_publish):
        print(f"Package file '{package_to_publish}' not found.")
        return

    url = f"http://localhost:{PORT}/{package_to_publish}"

    body_data = create_body_data(package_to_publish)
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, data=body_data, headers=headers)

    print(f"Request made: {response.request.method} {response.request.url}")
    print(f"Response received: {response.status_code} {response.reason}")
    if response.status_code == 201:
        print("Package published successfully.")
    else:
        print("Package publishing failed.")

if __name__ == "__main__":
    package_arg = sys.argv[1] if len(sys.argv) > 1 else None
    test_npm_server_package(package_arg)
