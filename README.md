python-couchdblogger
====================

Simple module for logging to CouchDB. 
Probably not best choise for logging backend, because CouchDB is not good with massive write operations. 

    https://pypi.python.org/pypi/couchdblogger

Usage:

    import couchdblogger

    logger = logging.getLogger('mylogger')
    logger.setLevel('ERROR')
    logger.addHandler(couchdblogger.CouchDBLogHandler())
   
Usage with ssl:

    import couchdblogger

    logger = logging.getLogger('mylogger')
    logger.setLevel('ERROR')
    logger.addHandler(couchdblogger.CouchDBLogHandler(ssl=True, request_args={"verify": True}))

Script to run tests:
--------------------

1- Install:

    python setup.py install
    pip install mock
    pip install nose

2- Run tests:

    python setup.py test

  or:

    nosetests -vv

Run nosetests with coverage:

    nosetests --with-coverage; coverage report

Tests:
-----

[![Build Status](https://drone.io/github.com/histrio/python-couchdblogger/status.png)](https://drone.io/github.com/histrio/python-couchdblogger/latest)
[![Requirements Status](https://requires.io/github/histrio/python-couchdblogger/requirements.png?branch=master)](https://requires.io/github/histrio/python-couchdblogger/requirements/?branch=master)
