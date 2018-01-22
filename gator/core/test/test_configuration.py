#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from core import configuration
from core.configuration import PathFinder, GatorConf


class TestGlobals(unittest.TestCase):

    def test_find_config_dir(self):
        path = configuration.find_config_dir()
        print(path)
        self.assertIn("/gator/conf", path)

        path = configuration.find_config_dir("test")
        print(path)
        self.assertIn("/gator/test", path)


class TestPathFinder(unittest.TestCase):

    def setUp(self):
        self.pf = PathFinder(dir_name="test")

    def tearDown(self):
        shutil.rmtree(self.pf.config_dir)
        pass

    def test_reads_and_writes_empty_list(self):
        self.assertIn("/gator/test", self.pf.config_dir)
        self.assertTrue(os.path.exists(self.pf.config_dir))
        self.pf.persist()
        self.assertTrue(os.path.exists(self.pf.config_file))

    def test_reads_and_writes_list(self):
        self.pf.append("abc/defg")
        self.pf.append("hij/klmn")
        self.pf.persist()

        pf2 = PathFinder(dir_name="test")
        self.assertEqual(pf2.path_list()[0], "abc/defg")
        self.assertEqual(pf2.path_list()[1], "hij/klmn")
        pf2.set_path_list([])
        pf2.persist()

        pf3 = PathFinder(dir_name="test")
        self.assertEqual(len(pf3.path_list()), 0)

    def test_existing_dirs(self):
        print(os.path.realpath(__file__))
        self.pf.append(os.path.realpath(__file__))
        print(self.pf.first_existing_dir())


class TestGatorConf(unittest.TestCase):

    def test_starts_with_none(self):
        gc = GatorConf()
        self.assertEqual(gc.resource_dir(), os.path.expanduser("~"))






