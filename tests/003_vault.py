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
        v2 = OP2Vault(self.I)

        v2.name(self.TEST_VAULT_NAME)
        v2.save()

        i = OP2Item(self.I)
        i.set("title",self.TEST_ITEM_TITLE )
        i.set("vault", self.TEST_VAULT_NAME)
        i.save()

    def test_01_new(self):
        v = OP2Vault(self.I)
        v.name(self.TEST_VAULT_NAME+"2")
        v.save()

        i2 = OP2Item(self.I)
        i2.set("title",self.TEST_ITEM_TITLE )
        i2.set("vault", self.TEST_VAULT_NAME+"2")
        i2.save()

        i3 = OP2Item(self.I)
        i3.set("title",self.TEST_ITEM_TITLE )
        i3.set("vault", self.TEST_VAULT_NAME+"2")
        i3.save()

        try:
            item = OP2Item(self.I, self.TEST_ITEM_TITLE, v.id)
            assert False
        except MultipleMatchesException:
            for i in self.I.items(self.TEST_ITEM_TITLE, vault=v.id):
                OP2Item(self.I, i["id"])



    def test_02_get_in_specific_vault(self):
        v = OP2Vault(self.I,  self.TEST_VAULT_NAME)
        OP2Item(self.I, self.TEST_ITEM_TITLE, vault=v.id)

    def test_2_new_url(self):

        v = OP2Vault(self.I,  self.TEST_VAULT_NAME)
        item = OP2Item(self.I)

        item.set('title', self.TEST_ITEM_TITLE+'url')
        item.set('vault',  v.id)
        item.set('url',  "http://lol.cat")
        item.set('username',  "username")
        item.set('password',  "password")
        item.set('notesPlain',  "notes here")
        item.set('tags',  ["tags", "go", "here"])
        item.save()
        time.sleep(3)

    def tearDown(self):
        try:
            v = OP2Vault(self.I, self.TEST_VAULT_NAME)
            v.delete()
        except:
            pass

        try:
            v2 = OP2Vault(self.I, self.TEST_VAULT_NAME+"2")
            v2.delete()
        except:
            pass

if __name__ == '__main__':
    unittest.main()
