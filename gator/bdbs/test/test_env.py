#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import unittest

import sys
from datetime import datetime

from bdbs.env import Repository


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

    def test_create(self):
        rep = Repository("test_db")
        db_env = rep.db_env()

        print(Repository.__name__.lower())

        # print(rep.db_home())

        bdb = rep.bdb("bar/test_file.bdb")

        bdb.put("test a", "foo_a")
        bdb.put("bla bla \n bla", "boring \t tango")
        bdb.put(None, "does it?") # stored as (b'', b'does it?')

        self.assertEqual(bdb.get("test a"), "foo_a")
        print(">>>>> get None", bdb.get(None))
        # print(bdb.get("test a"))
        # print(bdb.get("test a"))
        # print(bdb.get("test b"))  # None
        # print(bdb.get("test b", "Calcutta"))
        # print(bdb.get_both("test a", "foo_a"))
        # print(bdb.get_both("test b", "foo_a"))
        # print(bdb.get_size("test a"))
        # # print(bdb.get_size("test b"))
        # print("key_range", bdb.key_range("test a"))
        # print(bdb.has_key("test a"))
        # print(bdb.items_decoded())
        # print(bdb.keys_decoded())
        # print(bdb.values_decoded())

        # print(bdb.stat())

        # cursor = bdb.cursor()
        # print("first", cursor.first)
        # print("next", cursor.next())
        # print("next", cursor.next())
        # print("current", cursor.current())
        # print("next", cursor.next())
        # print("next", cursor.next())
        # print("current", cursor.current())
        # print("last", cursor.last())
        # print("current size", cursor.get_current_size())
        #print(cursor.current())
        my_list = list()
        my_list.append("foo")
        my_list.append("bar")
        bdb.put_list("my list", my_list)
        print(bdb.get_list("my list"))
        print(bdb.get("my list"))

        dt = datetime.today()
        print(dt)
        string = dt.strftime("%Y%m%d%H%M%S")
        print(string)
        dt2 = datetime.strptime(string, "%Y%m%d%H%M%S")
        print(dt2)

        rep.close()

    # def test_classic(self):
    #     # Part 1: Create database and insert 4 elements
    #     #
    #     filename = 'fruit'
    #
    #     # Get an instance of BerkeleyDB
    #     fruitDB = db.DB()
    #     # Create a database in file "fruit" with a Hash access method
    #     # 	There are also, B+tree and Recno access methods
    #     fruitDB.open(filename, None, db.DB_HASH, db.DB_CREATE)
    #
    #     # Print version information
    #     print(db.version())
    #     print("transactional:", fruitDB.get_transactional())
    #     print("keys:", fruitDB.keys())
    #     print("len:", len(fruitDB))
    #
    #     # Insert new elements in database
    #     fruitDB.put("apple".encode("utf-8"), "green, red".encode("utf-8"))
    #     fruitDB.put("orange".encode("utf-8"), "orange".encode("utf-8"))
    #     fruitDB.put("banana".encode("utf-8"), "yellow".encode("utf-8"))
    #     fruitDB.put("tomato".encode("utf-8"), "red".encode("utf-8"))
    #
    #     # Close database
    #     fruitDB.close()
    #
    #     # Part 2: Open database and write its contents out
    #     #
    #     fruitDB = db.DB()
    #     # Open database
    #     #	Access method: Hash
    #     #	set isolation level to "dirty read (read uncommited)"
    #     fruitDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)
    #
    #     # get database cursor and print out database content
    #     cursor = fruitDB.cursor()
    #     rec = cursor.first()
    #     while rec:
    #         print(rec[0].decode('utf-8'), rec[1].decode('utf-8'))
    #         rec = cursor.next()
    #     fruitDB.close()


