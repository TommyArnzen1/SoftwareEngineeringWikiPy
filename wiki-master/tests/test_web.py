from . import WikiBaseTestCase

import os

from flask import current_app
from flask import Flask
from flask import g
from flask import app
from wiki.web.user import UserManager
from wiki.web.user import User
class WebContentTestCase(WikiBaseTestCase):
    """
        Various test cases around web content.
    """

    def test_index_missing(self):
        """
            Assert the wiki will correctly play the content missing
            index page, if no index page exists.
        """
        rsp = self.app.get('/')
        assert b"You did not create any content yet." in rsp.data
        assert rsp.status_code == 200


TEST_FILE_PATH = '/home/cyjava2006/PycharmProjects/WikiPy/tests/'

class TestUserManager(WebContentTestCase):

    def setUp(self):
        super(TestUserManager, self).setUp()

    def test_invalid_authentication_method(self):
        m = UserManager(TEST_FILE_PATH)
        self.assertRaises(NotImplementedError, m.add_user, m, 'bobby', 12345, authentication_method='this will cause an error')

    def test_read(self):
        m = UserManager(TEST_FILE_PATH)
        self.assertIsNotNone(m.read)

    def test_add_user(self):
        m = UserManager(TEST_FILE_PATH)
        self.assertIsNotNone(m.add_user('thename', 'securepassword', authentication_method='hash'))

    def test_get_user(self):
        m = UserManager(TEST_FILE_PATH)
        self.assertIsNotNone(m.get_user('name'))

    def test_delete_user(self):
        m = UserManager(TEST_FILE_PATH)
        m.add_user('nick', 'securepassword', authentication_method='hash')
        self.assertTrue(m.delete_user('nick'))


class TestUser(WebContentTestCase):
    def setUp(self):
        super(TestUser, self).setUp()

    def test_get(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertIsNotNone(u.get('password'))

    def test_is_authenticated(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertTrue(u.is_authenticated())

    def test_is_active(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertTrue(u.is_active())

    def test_is_anonymous(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertFalse(u.is_anonymous())

    def test_get_id(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertEqual('name', u.get_id())

    def test_check_password(self):
        m = UserManager(TEST_FILE_PATH)
        u = m.get_user('name')
        self.assertTrue(u.check_password('1234'))
        self.assertFalse(u.check_password('dingdong'))
