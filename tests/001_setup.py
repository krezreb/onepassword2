#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json, os, sys, stat
import unittest
import logging
import tempfile

import os
import onepassword2
from onepassword2 import OP2Vault, OP2, OP2Item, OPException, MultipleMatchesException, NoVaultException, NoSuchItemException



class TestSetup(unittest.TestCase):

    def setUp(self):
        username = os.getenv('OP_ACCOUNT')
        password = os.getenv('OP_PASSWORD')
        hostname = os.getenv('OP_HOSTNAME')
        secret_key = os.getenv('OP_SECRET_KEY')
        setattr(onepassword2, 'DEBUG', True)
        self.I = OP2( username, password, secret_key, hostname)
        self.I.signin()
        self.TEST_NOTE_TITLE="unittest note "+os.path.basename(__file__)
        self.TEST_VAULT_NAME="unittest vault " +os.path.basename(__file__)

        v = OP2Vault(self.I, )

        v.name(self.TEST_VAULT_NAME)
        v.save()

        # dupe item 1
        item = OP2Item(self.I)
        item.set('title', self.TEST_NOTE_TITLE)
        item.set('vault', self.TEST_VAULT_NAME)
        item.save()

        # dupe item 2
        item = OP2Item(self.I)
        item.set('title', self.TEST_NOTE_TITLE)
        item.set('vault', self.TEST_VAULT_NAME)
        item.save()


        # no dupe item
        item = OP2Item(self.I)
        item.set('title', self.TEST_NOTE_TITLE+" no dupe")
        item.set('vault', self.TEST_VAULT_NAME)
        item.save()


    def test_delete_matching(self):
        for i in self.I.items(self.TEST_NOTE_TITLE):
            item = OP2Item(self.I, i)

            item.delete()

    def test_vaults(self):

        for v in self.I.vaults():
            print(v)

    def test_get_item(self):
        OP2Item(self.I, self.TEST_NOTE_TITLE+" no dupe")

    def test_item_not_exists(self):
        try:
            self.I.item("fgjhfghjfghjfghjfghjfgjfghj")
            assert False
        except NoSuchItemException:
            assert True

    def test_item_duplicate(self):
        try:
            self.I.item(self.TEST_NOTE_TITLE)
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

    def tearDown(self):
        try:
            v = OP2Vault(self.I, self.TEST_VAULT_NAME)
            v.delete()
        except:
            pass

if __name__ == '__main__':
    unittest.main()
