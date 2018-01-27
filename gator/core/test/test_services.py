#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from core import services


class ServicesTest(unittest.TestCase):

    def test_chunck_string(self):
        generator = services.chunk_string("abcdefghijklmnopqrstuvwxyz", 3)
        print("\n".join(list(generator)))