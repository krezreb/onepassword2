#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, sys, stat
import unittest
import logging
import tempfile

import os
import onepassword2
from onepassword2 import OP2, OP2Item, OP2Vault, MultipleMatchesException, NoVaultException

import time

class TestSetup(unittest.TestCase):

    def setUp(self):
        username = os.getenv('OP_ACCOUNT')
        password = os.getenv('OP_PASSWORD')
        hostname = os.getenv('OP_HOSTNAME')
        setattr(onepassword2, 'DEBUG', True)
        self.I = OP2( username, password, hostname)
        self.I.signin()
        self.TEST_VAULT_NAME="unittest vault "+os.path.basename(__file__)
        self.TEST_ITEM_TITLE="unittest item "+os.path.basename(__file__)

    def test_01_new(self):

        v = OP2Vault(self.I)

        v.name(self.TEST_VAULT_NAME)
        v.save()

        i = OP2Item(self.I)
        i.set("title",self.TEST_ITEM_TITLE )
        i.set("vault", self.TEST_VAULT_NAME)
        i.save()

    def test_03_delete_single(self):
        time.sleep(6)

        v = OP2Vault(self.I, self.TEST_VAULT_NAME)
        v.delete()


if __name__ == '__main__':
    unittest.main()
