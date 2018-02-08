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





