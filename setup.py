from setuptools import setup


setup(
    name = "crypto_mediator",
    version = "0.9.0",
    author = "Connor Wallace",
    author_email = "wallaconno@gmail.com",
    description = ('Client that allows communication between many crypto exchanges'),
    license = "MIT",
    keywords = "cryptocurrency client",
    url = "http://www.github.com/cowalla/mediator",
    packages=[
        ''
        'crypto_mediator',
        'crypto_mediator.clients',
        'crypto_mediator.clients.helpers',
        'crypto_mediator.clients.tests',
        'crypto_mediator.fixtures',
        'crypto_mediator.fixtures.bittrex',
        'crypto_mediator.fixtures.coinbase',
        'crypto_mediator.fixtures.gatecoin',
        'crypto_mediator.fixtures.liqui',
        'crypto_mediator.fixtures.poloniex',

    ],
    install_requires=[
        'cbpro==1.1.4',
        'coinbase==2.0.6',
        'liqui==1.0.1',
        'pytest==3.2.5',
        'python-dateutil==2.8.1',
        'requests==2.20.0',
    ],
    dependency_links=[
        'https://github.com/ericsomdahl/python-bittrex',
        'https://github.com/s4w3d0ff/python-poloniex',
    ]
)
