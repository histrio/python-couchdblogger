python-couchdblogger
====================


На скорую руку написал модуль для логирования в couchdb. Вероятноm, мало еще кому придет в голову писать логи в такю медленную на вставку БД, но все же.

    https://pypi.python.org/pypi/couchdblogger

Пример использования:

.. code:: python 
    :number-lines:

    import couchdblogger

    logger = logging.getLogger('mylogger')
    logger.setLevel('ERROR')
    logger.addHandler(couchdblogger.CouchDBLogHandler())

Run tests with:

    nosetests -vv

  or:

    ipython test/test_*.py

Run nosetests with coverage:

    nosetests --with-coverage; coverage report
