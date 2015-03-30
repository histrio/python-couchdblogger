'''
    File: test_couchdbsession_unit.py
    Author: Federico Gonzalez
    Description: Tests - CouchDBSession
'''
from mock import Mock, patch
import unittest

import os, sys
sys.path.insert(0, os.path.abspath("../src"))

from couchdblogger import CouchDBSession, requests


class CouchDBSessionTest(unittest.TestCase):

    def setUp(self):
        self.couchdb_session = CouchDBSession()

    def test_is_instance(self):
        self.assertTrue(isinstance(self.couchdb_session, CouchDBSession), "Is instance of CouchDBSession")
        self.assertTrue(issubclass(CouchDBSession, requests.Session), "Is subclass CouchDBSession of requests.Session")

    def test_exception(self):
        self.assertTrue(issubclass(CouchDBSession.CouchDBException, Exception), "Is subclass CouchDBException of Exception")

    def test_request_resp_200_ok(self):
        request_resp = Mock()
        request_resp.status_code = 200
        with patch('requests.Session.request', Mock(return_value=request_resp)) as requests_mock:
            resp = self.couchdb_session.post('http://localhost:5984/_session', data={
                'name': 'username',
                'password': 'password'
            })

            self.assertTrue(requests_mock.called, "")
            self.assertEqual(requests_mock.call_args[0][0].upper(), 'POST', "")
            self.assertEqual(requests_mock.call_args[0][1], 'http://localhost:5984/_session', "")
            self.assertTrue(requests_mock.call_args[1]['data'] is not None, "")
            self.assertEqual(requests_mock.call_args[1]['data']['name'], 'username', "")
            self.assertEqual(requests_mock.call_args[1]['data']['password'], 'password', "")
            self.assertEqual(len(requests_mock.call_args_list), 1, "")
            self.assertEqual(resp, request_resp, "")

    def test_request_resp_200_ok_with_verify(self):
        request_resp = Mock()
        request_resp.status_code = 200
        self.couchdb_session = CouchDBSession(request_args = {"verify": True})
        with patch('requests.Session.request', Mock(return_value=request_resp)) as requests_mock:
            resp = self.couchdb_session.post('https://localhost:5984/_session', data={
                'name': 'username',
                'password': 'password'
            })

            self.assertTrue(requests_mock.called, "")
            self.assertEqual(requests_mock.call_args[0][0].upper(), 'POST', "")
            self.assertEqual(requests_mock.call_args[0][1], 'https://localhost:5984/_session', "")
            self.assertTrue(requests_mock.call_args[1]['data'] is not None, "")
            self.assertEqual(requests_mock.call_args[1]['data']['name'], 'username', "")
            self.assertEqual(requests_mock.call_args[1]['data']['password'], 'password', "")
            self.assertTrue(requests_mock.call_args[1]['verify'], "")
            self.assertEqual(len(requests_mock.call_args_list), 1, "")
            self.assertEqual(resp, request_resp, "")

    def test_request_resp_404_not_found(self):
        request_resp = Mock()
        request_resp.status_code = 404
        with patch('requests.Session.request', Mock(return_value=request_resp)) as requests_mock:
            self.assertRaises(CouchDBSession.CouchDBException, lambda: self.couchdb_session.post('http://localhost:5984/_session', data={
                'name': 'username',
                'password': 'password'
            }))

            self.assertTrue(requests_mock.called, "")
            self.assertEqual(requests_mock.call_args[0][0].upper(), 'POST', "")
            self.assertEqual(requests_mock.call_args[0][1], 'http://localhost:5984/_session', "")
            self.assertTrue(requests_mock.call_args[1]['data'] is not None, "")
            self.assertEqual(requests_mock.call_args[1]['data']['name'], 'username', "")
            self.assertEqual(requests_mock.call_args[1]['data']['password'], 'password', "")
            self.assertEqual(len(requests_mock.call_args_list), 1, "")

    def test_request_resp_401_unauthorized(self):
        request_resp = Mock()
        request_resp.status_code = 401
        with patch('requests.Session.request', Mock(return_value=request_resp)) as requests_mock:
            self.assertRaises(CouchDBSession.CouchDBException,
                    lambda: self.couchdb_session.post('http://localhost:5984/_session', data={
                'name': 'username',
                'password': 'password'
            }))

            self.assertTrue(requests_mock.called, "")
            self.assertEqual(requests_mock.call_args[0][0].upper(), 'POST', "")
            self.assertEqual(requests_mock.call_args[0][1], 'http://localhost:5984/_session', "")
            self.assertTrue(requests_mock.call_args[1]['data'] is not None, "")
            self.assertEqual(requests_mock.call_args[1]['data']['name'], 'username', "")
            self.assertEqual(requests_mock.call_args[1]['data']['password'], 'password', "")
            self.assertEqual(len(requests_mock.call_args_list), 1, "")

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(CouchDBSessionTest))
