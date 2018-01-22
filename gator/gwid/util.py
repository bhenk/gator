#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtGui import QIcon

ICON_ARROW_DOWN = "arrow1-down.png"
ICON_ARROW_LEFT = "arrow1-left.png"
ICON_ARROW_UP = "arrow1-up.png"
ICON_ARROW_RIGHT = "arrow1-right.png"


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def icon(filename):
    path = os.path.join(application_home(), "gwid", "img", filename)
    return QIcon(path)