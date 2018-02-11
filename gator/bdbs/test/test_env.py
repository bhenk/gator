#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import sys
import unittest

from bdbs.store import Store


class TestRepository(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # logging:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

    def test_get_latest(self):
        store = Store("/Users/ecco/tmp/gator1/db")
        bdb = store.view_date_store().bdb
        for tup in bdb.get_keys_with_latest_values():
            print(tup[1], tup[0])

