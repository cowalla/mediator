# MEDIATOR
A meta client that makes interracting with several exchanges painless. Mediator knows how to interract with these exchanges so you don't have to.


### Getting started

pip install <mediator_tarball>

you will need to install other third-party clients to make this client work:
- python-bittrex: https://github.com/ericsomdahl/python-bittrex
- python-poloniex: https://github.com/s4w3d0ff/python-poloniex

### Use

Import the metaclient into your project, 

- `from crypto_mediator import CryptoMediator`

### Adding new exchanges to the MetaClient

- Add the new client library to the requirements.txt file
- Add the new client to the helper map in `client.py` and in `settings.py`
- Add a new fixtures folder for the endpoints you would like to support
  - format is `endpoint.py`, includes request_url and response in file.
- Add a client helper to helpers.py defining methods for the helper

### testing 
- `py.test crypto_mediator/clients/tests`

### example shell
- `python -i -m crypto_mediator.example`
