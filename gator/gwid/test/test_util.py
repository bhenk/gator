#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import locale
import unittest

from PyQt5.QtGui import QIcon
from gwid import util


class TestUtil(unittest.TestCase):

    def test_get_icon(self):
        icon = util.icon(util.ICON_ARROW_DOWN)
        self.assertIsInstance(icon, QIcon)


class TestLocale(unittest.TestCase):

    def test_locale(self):
        #locale.setlocale(locale.LC_ALL, 'nl_NL')
        # locale.setlocale(locale.LC_ALL, '')
        # print(locale.localeconv())
        # print(locale.currency(10000.00))
        print(locale.format_string("%d", 10000))
        print("{0:,g}".format(100000.00).replace(",", "."))