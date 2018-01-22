#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from PyQt5.QtGui import QIcon
from gwid import util


class TestUtil(unittest.TestCase):

    def test_get_icon(self):
        icon = util.icon(util.ICON_ARROW_DOWN)
        self.assertIsInstance(icon, QIcon)