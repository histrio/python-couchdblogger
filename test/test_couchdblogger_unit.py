'''
    File: test_couchdblogger_unit.py
    Author: Federico Gonzalez
    Description: Tests - CouchDBLogHandler
'''
from mock import Mock, patch
import unittest
import json


import sys, os
sys.path.insert(0, os.path.abspath("../src"))

from couchdblogger import CouchDBLogHandler, CouchDBSession, logging


class CouchDBLogHandlerTest(unittest.TestCase):

    def setUp(self):
        self.couchdb_handler = CouchDBLogHandler()
        self.record = Mock()
        self.record.name = 'process_name'
        self.record.msg = 'log to couchdb'
        self.record.levelname = 'level INFO'
        self.record.created = 1396988156

    def test_is_instance(self):
        self.assertTrue(isinstance(self.couchdb_handler, CouchDBLogHandler), "Is instance of CouchDBLogHandler")
        self.assertTrue(issubclass(CouchDBLogHandler, logging.StreamHandler), "Is subclass CouchDBLogHandler of logging.StreamHandler")

    @patch.object(logging.StreamHandler, '__init__')
    def test_init_username_none(self, *args):
        self.assertFalse(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'http://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://localhost:5984/logs', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")

    @patch.object(logging.StreamHandler, '__init__')
    def test_init_username_none_ssl_true(self, *args):
        self.couchdb_handler = CouchDBLogHandler(ssl=True)
        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'https://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'https://localhost:5984/logs', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")

    @patch.object(logging.StreamHandler, '__init__')
    @patch.object(CouchDBSession, 'get')
    def test_init_username_none_create_database_exist(self, *args):
        self.couchdb_handler = CouchDBLogHandler(create_database=True)
        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'http://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://localhost:5984/logs', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")
        self.assertTrue(CouchDBSession.get.called, "")
        self.assertEqual(CouchDBSession.get.call_args[0][0], 'http://localhost:5984/logs', "")

    @patch.object(logging.StreamHandler, '__init__')
    @patch.object(CouchDBSession, 'put')
    def test_init_username_none_create_database_not_exist(self, *args):

        def get_raise(_, url):
            self.assertEqual(url, 'http://localhost:5984/logs', "")
            raise CouchDBSession.CouchDBException
        CouchDBSession.get = get_raise

        self.couchdb_handler = CouchDBLogHandler(create_database=True)
        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'http://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://localhost:5984/logs', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")
        self.assertTrue(CouchDBSession.put.called, "")
        self.assertEqual(CouchDBSession.put.call_args[0][0], 'http://localhost:5984/logs', "")

    @patch.object(CouchDBSession, 'post')
    @patch.object(logging.StreamHandler, '__init__')
    def test_init_username_not_is_none(self, *args):
        self.assertFalse(logging.StreamHandler.__init__.called, "")
        self.assertFalse(CouchDBSession.post.called, "")

        self.couchdb_handler = CouchDBLogHandler(host='127.0.0.1', port=8080, database='logs-process', username='user', password='secret')

        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 8080, "")
        self.assertEqual(self.couchdb_handler.url, 'http://127.0.0.1:8080', "")
        self.assertEqual(self.couchdb_handler.database, 'logs-process', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://127.0.0.1:8080/logs-process', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")
        self.assertTrue(CouchDBSession.post.called, "")
        self.assertEqual(CouchDBSession.post.call_args[0][0], 'http://127.0.0.1:8080/_session', "")
        self.assertTrue(CouchDBSession.post.call_args[1]['data'] is not None, "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['name'], 'user', "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['password'], 'secret', "")

    @patch.object(CouchDBSession, 'post')
    @patch.object(logging.StreamHandler, '__init__')
    def test_init_username_not_is_none_and_ssl_true(self, *args):
        self.assertFalse(logging.StreamHandler.__init__.called, "")
        self.assertFalse(CouchDBSession.post.called, "")

        self.couchdb_handler = CouchDBLogHandler(host='127.0.0.1', port=8080, database='logs-process', username='user', password='secret', ssl=True)

        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 8080, "")
        self.assertEqual(self.couchdb_handler.url, 'https://user:secret@127.0.0.1:8080', "")
        self.assertEqual(self.couchdb_handler.database, 'logs-process', "")
        self.assertEqual(self.couchdb_handler.db_url, 'https://user:secret@127.0.0.1:8080/logs-process', "")
        self.assertTrue(isinstance(self.couchdb_handler.session, CouchDBSession), "")
        self.assertTrue(CouchDBSession.post.called, "")
        self.assertEqual(CouchDBSession.post.call_args[0][0], 'https://user:secret@127.0.0.1:8080/_session', "")
        self.assertTrue(CouchDBSession.post.call_args[1]['data'] is not None, "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['name'], 'user', "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['password'], 'secret', "")

    def test_format(self):
        left_data = json.loads(self.couchdb_handler.format(self.record))
        right_data = json.loads('{"logger": "process_name", "created": 1396988156, "message": "log to couchdb", "level": "level INFO"}')
        self.assertEqual(left_data, right_data, "")

    @patch.object(CouchDBSession, 'post')
    def test_emit(self, *args):
        self.couchdb_handler.emit(self.record)

        self.assertTrue(CouchDBSession.post.called, "")
        self.assertEqual(CouchDBSession.post.call_args[0][0], 'http://localhost:5984/logs', "")
        self.assertTrue(CouchDBSession.post.call_args[1]['data'] is not None, "")
        self.assertTrue(CouchDBSession.post.call_args[1]['headers'] is not None, "")

        left_data = json.loads(CouchDBSession.post.call_args[1]['data'])
        right_data = json.loads('{"logger": "process_name", "created": 1396988156, "message": "log to couchdb", "level": "level INFO"}')

        self.assertEqual(left_data, right_data, "")

        self.assertEqual(CouchDBSession.post.call_args[1]['headers']['Content-type'], 'application/json', "")

    def test_new_format(self):

        def format_function(record):
            json_to_post = json.dumps(dict(
                message=record.msg,
                log_level=record.levelname,
                name_logger=record.name,
                extra_message='message',
                log_date_time=record.asctime
            ))
            return json_to_post

        self.couchdb_handler.new_format(format_function)

        self.assertEqual(id(format_function), id(self.couchdb_handler.format), "")

    def test_new_format_with_lambda(self):
        id_format = id(self.couchdb_handler.format)
        self.couchdb_handler.new_format(lambda record: json.dumps(dict(message=record.msg, log_level=record.levelname, name_logger=record.name, extra_message='message', log_date_time=record.asctime)))

        self.assertNotEqual(id_format, id(self.couchdb_handler.format), "")


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(CouchDBLogHandlerTest))
