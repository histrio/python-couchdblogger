Python-couchdblogger
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

Run tests with:

    nosetests -vv

  or:

    ipython test/test_*.py

Run nosetests with coverage:

    nosetests --with-coverage; coverage report

Tests:
-----

[![Build Status](https://drone.io/github.com/FedeG/python-couchdblogger/status.png)](https://drone.io/github.com/FedeG/python-couchdblogger/latest)
