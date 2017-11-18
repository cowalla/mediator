### Getting started

- install the requirements: `pip install -r requirements.txt`
- import the metaclient into your project, `from mediator.clients.client import MetaClient`


### Adding new exchanges to the MetaClient

- Add the new client library to the requirements.txt file
- Add the new client to the helper map in `client.py` and in `settings.py`
- Add a new fixtures folder for the endpoints you would like to support
  - format is `endpoint.py`, includes request_url and response in file.
- Add a client helper to helpers.py defining methods for the helper

