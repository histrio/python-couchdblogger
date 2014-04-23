'''
File: couchdblogger.py
Author: Rinat F Sabitov, Federico Gonzalez
Description:
'''
import logging
import json
import requests


class CouchDBSession(requests.Session):
    """
        CouchDBSession that inherits from requests.Session

        CouchDBSession:
            Session handling orders couchdb

        requests.Session:
            Provides cookie persistence, connection-pooling, and configuration.
    """

    class CouchDBException(Exception):
        """
            CouchDBException that inherits from Exception

            CouchDBException:
                Exception error when response code greater than 400

            Exception:
                Common base class for all non-exit exceptions.
        """
        pass

    def request(self, *args, **kwargs):
        """
        Constructs a :class:`Request <Request>`, prepares it and sends it.
        Returns :class:`Response <Response>` object.
        In the case of having a code greater than 400 returns CouchDBException

        Args:
            :param method: method for the new :class:`Request` object.
            :param url: URL for the new :class:`Request` object.

        Kwargs:
        :param params: (optional) Dictionary or bytes to be sent in the query
            string for the :class:`Request`.
        :param data: (optional) Dictionary or bytes to send in the body of the
            :class:`Request`.
        :param headers: (optional) Dictionary of HTTP Headers to send with the
            :class:`Request`.
        :param cookies: (optional) Dict or CookieJar object to send with the
            :class:`Request`.
        :param files: (optional) Dictionary of 'filename': file-like-objects
            for multipart encoding upload.
        :param auth: (optional) Auth tuple or callable to enable
            Basic/Digest/Custom HTTP Auth.
        :param timeout: (optional) Float describing the timeout of the
            request.
        :param allow_redirects: (optional) Boolean. Set to True by default.
        :param proxies: (optional) Dictionary mapping protocol to the URL of
            the proxy.
        :param stream: (optional) whether to immediately download the response
            content. Defaults to ``False``.
        :param verify: (optional) if ``True``, the SSL cert will be verified.
            A CA_BUNDLE path can also be provided.
        :param cert: (optional) if String, path to ssl client cert file (.pem).
            If Tuple, ('cert', 'key') pair.
        """
        resp = super(CouchDBSession, self).request(*args, **kwargs)
        if resp.status_code >= 400:
            raise self.CouchDBException(resp.text)
        return resp


class CouchDBLogHandler(logging.StreamHandler):
    """
        CouchDBLogHandler that inherits from logging.StreamHandler

        logging.StreamHandler:
            A handler class which writes logging records,
            appropriately formatted, to a stream.
            Note that this class does not close the stream, as
            sys.stdout or sys.stderr may be used.
    """

    def __init__(self, host='localhost', port=5984, database='logs', create_database=False,
        username=None, password=None):
        """
            Initialize the couchdb handler

        :param host: host of couchdb for logging
        :param port: port of couchdb for logging
        :param database: database's name for logging
        :param username: user's name for logging in the database
        :param password: password for logging in the database
        :param create_database: boolean to create the database if it does not exist
        """
        super(CouchDBLogHandler, self).__init__()

        self.database = database
        self.port = port

        self.url = "http://%(host)s:%(port)d" % dict(
            host=host,
            port=port,
        )

        self.db_url = "%(url)s/%(database)s" % dict(
            url=self.url,
            database=database
        )

        self.session = CouchDBSession()
        if username:
            self.session.post(self.url+'/_session', data={
                'name': username,
                'password': password
            })

        if create_database:
            try:
                self.session.get(self.db_url)
            except CouchDBSession.CouchDBException:
                self.session.put(self.db_url)

    def new_format(self, format_function):
        """
            Change the format logging

        :param format_function: function to generate couchdb logs from logging record
        
        REQUIRED: The function must return a json.dumps to post in couchdb
        
        """
        self.format = format_function

    def format(self, record):
        """
            Format a logging record to couchdb record

        :param record: loggging record (LogRecord)
        The useful attributes in a LogRecord are described by:

        %(name)s            Name of the logger (logging channel)
        %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                            WARNING, ERROR, CRITICAL)
        %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                            "WARNING", "ERROR", "CRITICAL")
        %(pathname)s        Full pathname of the source file where the logging
                            call was issued (if available)
        %(filename)s        Filename portion of pathname
        %(module)s          Module (name portion of filename)
        %(lineno)d          Source line number where the logging call was issued
                            (if available)
        %(funcName)s        Function name
        %(created)f         Time when the LogRecord was created (time.time()
                            return value)
        %(asctime)s         Textual time when the LogRecord was created
        %(msecs)d           Millisecond portion of the creation time
        %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        %(thread)d          Thread ID (if available)
        %(threadName)s      Thread name (if available)
        %(process)d         Process ID (if available)
        %(message)s         The result of record.getMessage(), computed just as
                            the record is emitted
        """
        return json.dumps(dict(
            message=record.msg,
            level=record.levelname,
            created=record.created,
            logger=record.name
        ))

    def emit(self, record):
        """
            Emit a logging record

        :param record: loggging record
        """
        headers = {'Content-type': 'application/json'}
        self.session.post(self.db_url, data=self.format(record),
            headers=headers
        )
