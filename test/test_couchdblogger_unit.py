'''
    File: test_couchdblogger_unit.py
    Author: Federico Gonzalez
    Description: Tests - CouchDBLogHandler
'''
from mock import Mock, patch
from src.couchdblogger import CouchDBLogHandler, CouchDBSession, logging
import unittest


class CouchDBLogHandlerTest(unittest.TestCase):

    def setUp(self):
        self.couchdb_handler = CouchDBLogHandler()
        self.record = Mock()
        self.record.name = 'process_name'
        self.record.msg = 'log to couchdb'
        self.record.levelname = 'level INFO'
        self.record.created = 1396988156

    def test_is_instance(self):
        self.assertIsInstance(self.couchdb_handler, CouchDBLogHandler, "Is instance of CouchDBLogHandler")
        self.assertTrue(issubclass(CouchDBLogHandler, logging.StreamHandler), "Is subclass CouchDBLogHandler of logging.StreamHandler")

    @patch.object(logging.StreamHandler, '__init__')
    def test_init_username_none(self, *args):
        self.assertFalse(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'http://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://localhost:5984/logs', "")
        self.assertIsInstance(self.couchdb_handler.session, CouchDBSession, "")

    @patch.object(logging.StreamHandler, '__init__')
    @patch.object(CouchDBSession, 'get')
    def test_init_username_none_create_database_exist(self, *args):
        self.couchdb_handler = CouchDBLogHandler(create_database=True)
        self.assertTrue(logging.StreamHandler.__init__.called, "")
        self.assertEqual(self.couchdb_handler.port, 5984, "")
        self.assertEqual(self.couchdb_handler.url, 'http://localhost:5984', "")
        self.assertEqual(self.couchdb_handler.database, 'logs', "")
        self.assertEqual(self.couchdb_handler.db_url, 'http://localhost:5984/logs', "")
        self.assertIsInstance(self.couchdb_handler.session, CouchDBSession, "")
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
        self.assertIsInstance(self.couchdb_handler.session, CouchDBSession, "")
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
        self.assertIsInstance(self.couchdb_handler.session, CouchDBSession, "")
        self.assertTrue(CouchDBSession.post.called, "")
        self.assertEqual(CouchDBSession.post.call_args[0][0], 'http://127.0.0.1:8080/_session', "")
        self.assertIsNotNone(CouchDBSession.post.call_args[1]['data'], "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['name'], 'user', "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data']['password'], 'secret', "")

    def test_format(self):
        self.assertEqual(self.couchdb_handler.format(self.record), '{"logger": "process_name", "created": 1396988156, "message": "log to couchdb", "level": "level INFO"}', "")

    @patch.object(CouchDBSession, 'post')
    def test_emit(self, *args):
        self.couchdb_handler.emit(self.record)

        self.assertTrue(CouchDBSession.post.called, "")
        self.assertEqual(CouchDBSession.post.call_args[0][0], 'http://localhost:5984/logs', "")
        self.assertIsNotNone(CouchDBSession.post.call_args[1]['data'], "")
        self.assertIsNotNone(CouchDBSession.post.call_args[1]['headers'], "")
        self.assertEqual(CouchDBSession.post.call_args[1]['data'], '{"logger": "process_name", "created": 1396988156, "message": "log to couchdb", "level": "level INFO"}', "")
        self.assertEqual(CouchDBSession.post.call_args[1]['headers']['Content-type'], 'application/json', "")

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(CouchDBLogHandlerTest))
