# npm Registry Publish Test Server

## Purpose
The "npm Registry Publish Test Server" is designed to implement a local
testing environment for testing npm package publication. It functions as a test
package repository, serving the sole purpose of facilitating the local testing
of package publication via npm. 

### Key Features
- Provides a local disk test package repository server.
- Supports HTTP PUT requests exclusively for package publication testing.
- Emphasizes local testing and does not aim to serve as a fully-fledged package repository.

The primary intention of this software is to enable the ability to test the
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
127.0.0.1 - - [13/Nov/2023 16:22:36] "PUT /calculator-1.0.0.tgz HTTP/1.1" 201 -
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
Request made: PUT http://localhost:8077/calculator-1.0.0.tgz
Response received: 201 Created
Package published successfully.
```

```bash
$ python npm_server.py
Server running on port 8077...
127.0.0.1 - - [13/Nov/2023 16:22:36] "PUT /calculator-1.0.0.tgz HTTP/1.1" 201 -
^C
KeyboardInterrupt received. Server shutting down.
$ tree stored_packages/
stored_packages/
|-- calculator-1.0.0.json
`-- calculator-1.0.0.tgz

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

`npm publish` requires authentication, but the npm Registry Publish Test Server
does not require authentication. A dummy token can be used.

```bash
//localhost:8077/:_authToken=NONE1234
```

When `npm publish` is ran, the package is sent to the specified registry for
storage and distribution. This configuration assumes the npm Registry Publish
Test Server is listening on localhost port 8077.

## License

Apache License 2.0, see [LICENSE](https://www.apache.org/licenses/LICENSE-2.0).

This program is free software
