#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
import unittest

from bdbs.store import Store
from core.services import Format


class TestViewDateStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store = Store("store_test")
        # logging:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_gator1_db(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        vds = store.view_date_store()
        sequence = vds.sequence_count(total=4559)
        print(len([x for x in sequence if x == 0]))
        print(len([x for x in sequence if x != 0]))
        print(len(vds.bdb))
        # print(len(sequence))
        # print(min(sequence))
        # print("{0:.2f}".format(mean(sequence)))

    def test_count_view_dates(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        vds = store.view_date_store()
        for resource in vds.resource_generator()():
            count_view_dates = len(resource.view_dates())
            if count_view_dates > 2:
                print(count_view_dates, resource.filename())
        print("len views", len(vds.bdb))
        print(store.repository.db_home())

    def test_set_viewed(self):
        print(os.path.split("bla.txt"))
        print(os.path.splitext("bla.tst")[0])

    def test_acme(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        ads = store.acme_date_store()

        #
        for resource in ads.resource_generator()():
            print(resource.acme_dates(fmt=Format.DATE_FULL), resource.filename())

    def test_replicate(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        store.replicate()