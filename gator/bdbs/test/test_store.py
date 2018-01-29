#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import unittest

import sys
from bdbs.obj import Resource
from bdbs.store import Store




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

    def test_update(self):
        vds = self.store.view_date_store()
        resource = Resource("long/file/name.pdf")

        print(vds.get(resource))

        # vds.set_viewed(resource)
        print(resource.view_dates())

        resource2 = Resource("long/file/name.pdf")
        vds.update(resource2)
        print(resource2.view_dates())
        print(resource2.view_dates("%Y-%m-%d"))

    def test_gator1_db(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        vds = store.view_date_store()
        for item in vds.bdb.items_decoded():
            print(item)

    def test_count_view_dates(self):
        store = Store("/Volumes/Backup/20171217/gator2/db")
        vds = store.view_date_store()
        for resource in vds.resource_generator()():
            if resource.count_view_dates() > 1:
                print(resource.count_view_dates(), resource.filename())
        print("max views", vds.max_views())



    def test_set_viewed(self):
        r1 = Resource("1")
        r2 = Resource("2")
        r3 = Resource("3")
        vds = self.store.view_date_store()

        vds.set_viewed(r1)
        vds.set_viewed(r2)
        vds.set_viewed(r3)

        for item in vds.bdb.items_decoded():
            print(item)
