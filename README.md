# npm Registry Publish Test Server

## Purpose
The "npm Registry Publish Test Server" is designed to offer developers a local
testing environment for testing npm package publication. It functions as a test
package repository, serving the sole purpose of facilitating the local testing
of package publication via npm. 

### Key Features
- Provides a local disk test package repository server.
- Supports HTTP POST requests exclusively for package publication testing.
- Emphasizes local testing and does not aim to serve as a fully-fledged package repository.

The primary intention of this software is to enable developers to test the
publication process without interacting with a live or production-level
package repository. 

## Installation

To install the "npm Registry Publish Test Server," follow these steps:

1. Clone the repository to your local disk:
   ```bash
   git clone https://github.com/rglaue/npm-registry-publish-test-server.git
   cd npm-publish-package-test-server
   ```

2. Install the necessary dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

Execute `npm_server.py` to start the local test package repository server:

```bash
$ python npm_server.py
Server running on port 8077...
127.0.0.1 - - [13/Nov/2023 16:22:36] "POST /calculator-1.0.0.tgz HTTP/1.1" 201 -
^C
KeyboardInterrupt received. Server shutting down.
```

### Building the Calculator Package

Run the `calculator_build.sh` script to create the `calculator-1.0.0.tgz` package:

```bash
$ cd test
$ bash calculator_build.sh  # created calculator-1.0.0.tgz
```

### Testing the Server

Run `npm_publish.py` to test the `npm_server.py` with the default `calculator-1.0.0.tgz` package. You can also specify a different package by providing its relative path as an argument:

```bash
$ cd test
$ python npm_publish.py your-package.tgz  # Specify your package
$ python npm_publish.py  # Uses default package 'calculator-1.0.0.tgz'
Request made: POST http://localhost:8077/calculator-1.0.0.tgz
Response received: 201 Created
Package published successfully.
```

```bash
$ python npm_server.py
Server running on port 8077...
127.0.0.1 - - [13/Nov/2023 16:22:36] "POST /calculator-1.0.0.tgz HTTP/1.1" 201 -
^C
KeyboardInterrupt received. Server shutting down.
$ tree stored_packages/
stored_packages/
└── calculator-1.0.0.tgz

1 directory, 1 file
```

## Configuration with an npm project

In the `package.json` file, configure the `"registry"` property within
`"publishConfig"` to specify a custom registry URL to where npm will
publish packages. For example:

```json
  "publishConfig": {
    "registry": "http://localhost:8077"
  }
```

This ensures that when developers run `npm publish`, the package is sent to the
specified registry for storage and distribution. This configuration assumes the
npm Registry Publish Test Server is listening on localhost port 8077.

## Deprecation of Python CGI and Implemented Solution

### Deprecation of `cgi` Module
The `cgi` module, aimed at supporting Common Gateway Interface (CGI) scripts,
has been marked for deprecation. The module's approach in handling incoming
requests by creating new processes for each request has been identified as 
inefficient. As noted in PEP 206, the module is regarded as:

> “[…] poorly designed and now deemed near-impossible to fix (cgi) […].”

Because the `cgi` package is deprecated, the "npm Registry Publish 
Test Server" introduces an alternative approach.

**If using the Python CGI package, it would be as follows**

```python
import cgi
import shutil

class PackageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_type, _ = cgi.parse_header(self.headers.get('content-type'))
        if content_type == 'multipart/form-data':
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            if 'file' in form_data:
                file_item = form_data['file']
                if file_item.file:
                    package_name = file_item.filename
                    storage_path = os.path.join(os.path.dirname(__file__), 'stored_packages')
                    os.makedirs(storage_path, exist_ok=True)

                    with open(os.path.join(storage_path, package_name), 'wb') as f:
                        shutil.copyfileobj(file_item.file, f)

                    self.send_response(201)
                    self.end_headers()
                    self.wfile.write(f"Package {package_name} stored successfully".encode())
                    return

        self.send_response(400)
        self.end_headers()
        self.wfile.write("Invalid request".encode())
```

**Without using the Python CGI package, it is implemented as follows**

```python
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
```

## License

Apache License 2.0, see [LICENSE](https://www.apache.org/licenses/LICENSE-2.0).

This program is free software
