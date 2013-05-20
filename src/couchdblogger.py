'''
File: couchdblogger.py
Author: Rinat F Sabitov
Description:
'''
import logging
import json
import requests

class CouchDBSession(requests.Session):

    class CouchDBException(Exception):
        pass

    def request(self, *args, **kwargs):
        resp = super(CouchDBSession, self).request(*args, **kwargs)
        if resp.status_code >= 400:
            raise self.CouchDBException(resp.text)
        return resp



class CouchDBLogHandler(logging.StreamHandler):

    def __init__(self, host='localhost', port=5984, database='logs',
        username=None, password=None):
        super(CouchDBLogHandler, self).__init__()

        self.database = database
        self.port = port
        self.database = database

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
            self.session.PUT(self.url+'/_session', data={
                name:username,
                password:password
            })

    def format(self, record):
        return json.dumps(dict(
            message = record.msg,
            level = record.levelname,
            created = record.created,
            logger = record.name

        ))

    def emit(self, record):
        headers = {'Content-type': 'application/json'}
        self.session.post(self.db_url, data=self.format(record),
            headers=headers
        )

