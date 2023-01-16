#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, sys, stat
import unittest
import logging
import tempfile

import os
import onepassword2
from onepassword2 import OP2, OP2Item, OPException, MultipleMatchesException, NoVaultException



class TestSetup(unittest.TestCase):

    def setUp(self):
        username = os.getenv('OP_ACCOUNT')
        password = os.getenv('OP_PASSWORD')
        hostname = os.getenv('OP_HOSTNAME')
        setattr(onepassword2, 'DEBUG', True)
        self.I = OP2( username, password, hostname)
        self.I.signin()
        self.TEST_NOTE_TITLE="unittest note"

    def test_delete_matching(self):
        for i in self.I.items(self.TEST_NOTE_TITLE):
            item = OP2Item(self.I, i)

            item.delete()

    def test_vaults(self):

        for v in self.I.vaults():
            print(v)

    def test_item(self):
        item = OP2Item(self.I, 's2n7wijs7awluzfbngj4nur4u4')

    def test_item_not_exists(self):
        try:
            self.I.item("lol")
            assert False
        except OPException:
            assert True

    def test_item_duplicate(self):
        try:
            self.I.item("install-upgrade-pcf.secrets.yml")
            assert False
        except MultipleMatchesException:
            assert True

    def test_new_item_no_vault(self):
        item = OP2Item(self.I)

        item.set('title', self.TEST_NOTE_TITLE)

        try:
            item.save()
            assert False
        except NoVaultException:
            assert True

if __name__ == '__main__':
    unittest.main()