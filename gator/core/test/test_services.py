#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from core import services
from core.services import Stat


class ServicesTest(unittest.TestCase):

    def test_chunck_string(self):
        generator = services.chunk_string("abcdefghijklmnopqrstuvwxyz", 3)
        print("\n".join(list(generator)))


class StatTest(unittest.TestCase):

    def test_format(self):
        stat = Stat(range(0, 100, 2))
        print(stat.to_string(" | ", decimals=5))

        stat = Stat([])
        print(stat.to_string(" | "))

        stat = Stat([6, 5])
        print(stat.to_string(" | "))