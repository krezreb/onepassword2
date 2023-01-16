#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, sys, stat
import unittest
import logging
import tempfile

import os
import onepassword2
from onepassword2 import OP2, OP2Item, OPException, MultipleMatchesException, NoVaultException

import time

class TestSetup(unittest.TestCase):

    def setUp(self):
        username = os.getenv('OP_ACCOUNT')
        password = os.getenv('OP_PASSWORD')
        hostname = os.getenv('OP_HOSTNAME')
        setattr(onepassword2, 'DEBUG', True)
        self.I = OP2( username, password, hostname)
        self.I.signin()
        self.TEST_NOTE_TITLE="unittest note"


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
        except OPException:
            assert True


if __name__ == '__main__':
    unittest.main()
