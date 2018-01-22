#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys

import pkg_resources
from PyQt5.QtGui import QIcon

LOG = logging.getLogger(__name__)

ICON_ARROW_DOWN = "img/arrow1-down.png"
ICON_ARROW_LEFT = "img/arrow1-left.png"
ICON_ARROW_UP = "img/arrow1-up.png"
ICON_ARROW_RIGHT = "img/arrow1-right.png"


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def icon(filename):
    path = pkg_resources.resource_filename(__name__, filename)
    if not os.path.exists(path):
        LOG.warning("File not found: %s" % path)
    return QIcon(path)


