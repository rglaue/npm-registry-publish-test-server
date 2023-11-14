import requests
import sys
import os

DEFAULT_PACKAGE = "calculator-1.0.0.tgz"
PORT = 8077

def test_npm_server_package(package_path=None):
    package_to_publish = package_path if package_path else DEFAULT_PACKAGE

    if not os.path.exists(package_to_publish):
        print(f"Package file '{package_to_publish}' not found.")
        return

    url = f"http://localhost:{PORT}/{os.path.basename(package_to_publish)}"

    with open(package_to_publish, 'rb') as package_file:
        files = {'file': package_file}
        response = requests.post(url, files=files)

        print(f"Request made: {response.request.method} {response.request.url}")
        print(f"Response received: {response.status_code} {response.reason}")
        if response.status_code == 201:
            print("Package published successfully.")
        else:
            print("Package publishing failed.")

if __name__ == "__main__":
    package_arg = sys.argv[1] if len(sys.argv) > 1 else None
    test_npm_server_package(package_arg)
