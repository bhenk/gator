#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from inspect import stack

import sys


class TestLocale(unittest.TestCase):

    def test_locale(self):
        # locale.setlocale(locale.LC_ALL, 'nl_NL')
        # locale.setlocale(locale.LC_ALL, '')
        # print(locale.localeconv())
        # print(locale.currency(10000.00))
        # print(locale.format_string("%d", 10000))
        # print("{0:,g}".format(100000.00).replace(",", "."))
        # line = sys._getframe().f_lineno
        # print(line)
        # from inspect import currentframe, getframeinfo
        #
        # frame_info = getframeinfo(currentframe())
        #
        # print(frame_info.filename, frame_info.lineno)
        # print(getouterframes(currentframe()))
        # print(stack())
        for frame_info in stack()[1:4]:
            print(frame_info)

    def test_go_test(self):
        self.test_locale()

    def test_x(self):
        self.test_go_test()
