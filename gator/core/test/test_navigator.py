#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from core.navigator import Resources


class TestResources(unittest.TestCase):

    def test_resources(self):
        print(Resources.filter_list())


