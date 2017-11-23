### Getting started

pip install <mediator_tarball>

also install these requirements
- https://github.com/s4w3d0ff/python-poloniex/archive/v0.4.6.zip
- git+https://github.com/ericsomdahl/python-bittrex.git

- install the requirements: `pip install -r requirements.txt`
- import the metaclient into your project, `from crypto_mediator import CryptoMediator`


### Adding new exchanges to the MetaClient

- Add the new client library to the requirements.txt file
- Add the new client to the helper map in `client.py` and in `settings.py`
- Add a new fixtures folder for the endpoints you would like to support
  - format is `endpoint.py`, includes request_url and response in file.
- Add a client helper to helpers.py defining methods for the helper

### testing 
- `py.test clients/tests`

### example shell
- `python example.py`
