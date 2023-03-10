#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, sys, stat
import unittest
import logging
import tempfile

import os
import onepassword2
from onepassword2 import OP2, OP2Item, OPException, MultipleMatchesException, NoVaultException, NoSuchItemException

import time

class TestSetup(unittest.TestCase):

    def setUp(self):
        username = os.getenv('OP_ACCOUNT')
        password = os.getenv('OP_PASSWORD')
        hostname = os.getenv('OP_HOSTNAME')
        secret_key = os.getenv('OP_SECRET_KEY')
        setattr(onepassword2, 'DEBUG', True)
        self.I = OP2( username, password, secret_key, hostname)
        self.I.signin()
        self.TEST_VAULT_NAME="unittest vault " +os.path.basename(__file__)
        self.TEST_NOTE_TITLE="unittest note " +os.path.basename(__file__)

    def test_1_delete_matching(self):
        for i in self.I.items(self.TEST_NOTE_TITLE):
            item = OP2Item(self.I, i)

            item.delete()

    def test_2_new_item(self):

        item = OP2Item(self.I)

        item.set('title', self.TEST_NOTE_TITLE)
        item.set('vault', "Private")
        item.save()
        time.sleep(3)



    def test_3_delete_single(self):
        item = OP2Item(self.I, self.TEST_NOTE_TITLE)
        item.delete()

        try:
            item = OP2Item(self.I, self.TEST_NOTE_TITLE)
            assert False
        except NoSuchItemException:
            assert True


if __name__ == '__main__':
    unittest.main()
