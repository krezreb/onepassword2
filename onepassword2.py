#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import argparse
from subprocess import Popen, PIPE
import os, json

class RunException(Exception):
    pass

def run(cmd, splitlines=False, env=None, raise_exception=False):
    # you had better escape cmd cause it's goin to the shell as is
    if env == None:
        env = os.environ.copy()
    proc = Popen([cmd], stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True, env=env)
    out, err = proc.communicate()
    if splitlines:
        out_split = []
        for line in out.split("\n"):
            line = line.strip()
            if line != '':
                out_split.append(line)
        out = out_split
    exitcode = int(proc.returncode)
    if raise_exception and exitcode != 0:
        raise RunException(err)
    return (out, err, exitcode)

class OP2():

    def __init__(self, username, password, hostname):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.session_token = None

    def status(self):
        if self.session_token == None:
            return False
        try:
            self.vaults()
            return True
        except RunException:
            self.session_token = None
            return False

    def signin(self):
        if self.status():
            return
        
        run("op account forget  --all 2> /dev/null")

        env2 = os.environ.copy()

        env2["OP_PASSWORD"] = self.password
        env2["OP_ACCOUNT"] = self.username
        env2["OP_HOSTNAME"] = self.hostname
        run('echo "$OP_PASSWORD" | op account add --shorthand $OP_ACCOUNT --address "$OP_HOSTNAME" --email "$OP_ACCOUNT" 2> /dev/null', env=env2)
        out, err, retcode = run('echo $OP_PASSWORD | op signin --account $OP_ACCOUNT -f', splitlines=True, env=env2)
        k,v = out[0].split("=",1)
        k = k[7:]
        v = v[1:-1]
        self.session_token = (k,v)

    def _decode(self, cmd):
        self.signin()

        env2 = os.environ.copy()
        env2[self.session_token[0]] = self.session_token[1]

        out, err, exitcode = run(cmd, env=env2)

        return json.loads(out)

    def _edit(self, data):
        cmd = "op item edit {} ".format(data["id"])
        cmd += " --title \"{}\" ".format(data["title"])
        if "urls" in data:
            cmd += " --url \"{}\" ".format(data["urls"][0]["href"])

        if "tags" in data:
            if type(data["tags"]) is list:
                cmd += " --tags \"{}\" ".format(",".join(data["tags"]))
            else:
                cmd += " --tags \"{}\" ".format(data["tags"])

        for field in data["fields"]:
            if "value" in field:
                cmd += " '{}={}' ".format(field['id'], field["value"])

        self.signin()

        env2 = os.environ.copy()
        env2[self.session_token[0]] = self.session_token[1]

        out, err, exitcode = run(cmd, env=env2)
        

    def _list(self, thing):
        cmd = "op {} list --format=json".format(thing)
        return self._decode(cmd)

    def _get(self, thing, id):
        cmd = "op {} get \"{}\" --format=json".format(thing, id)
        return self._decode(cmd)

    def _list_get(self, thing):
        for l1 in self._list(thing):
            id = l1["id"]
            yield self._get(thing, id)

    def vaults(self):
        return self._list_get("vault")

    def documents(self):
        return self._list_get("document")

    def items(self):
        return self._list_get("item")

    def item(self, item, as_obj=False):
        if type(item) is dict:
            i = self._get("item", item["id"])
        else:
            # item is a string with the item id
            i = self._get("item", item)

        if as_obj:
            I = OP2Item(op2=self, item=i)
            return I

        return i


class OP2Item():
    def __init__(self, op2: OP2, item) -> None:
        self.op2 = op2
        self.item = item

    def save(self):
        self.op2._edit(self.item)

    def set(self, k, v):
        if k in ("tags", "title"):
            self.item[k] = v
            return True

        if "fields" in self.item:
            for f in self.item["fields"]:
                if f["id"] == k:
                    f["value"] = v
                    return True

        return False        

    def get(self, k):
        if k in ("tags", "title"):
            try:
                return self.item[k]
            except KeyError:
                return None

        if "fields" in self.item:
            for f in self.item["fields"]:
                if f["id"] == k:
                    return f["value"]

        return None  
