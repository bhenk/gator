#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

import pkg_resources
from PyQt5.QtGui import QIcon

LOG = logging.getLogger(__name__)


ICON_ARROW_DOWN = "img/arrow1-down.png"
ICON_ARROW_LEFT = "img/arrow1-left.png"
ICON_ARROW_UP = "img/arrow1-up.png"
ICON_ARROW_RIGHT = "img/arrow1-right.png"


def icon(filename):
    path = pkg_resources.resource_filename(__name__, filename)
    if not os.path.exists(path):
        LOG.warning("File not found: %s" % path)
    return QIcon(path)


class GIcon(object):

    @staticmethod
    def plus(): return icon("img/plus-sign.png")

    @staticmethod
    def minus(): return icon("img/minus.png")

    @staticmethod
    def arr2_up(): return icon("img/arrow2-up.png")

    @staticmethod
    def arr2_down(): return icon("img/arrow2-down.png")

    @staticmethod
    def arr_left(): return icon("img/arrow1-left.png")

    @staticmethod
    def arr_up(): return icon("img/arrow1-up.png")

    @staticmethod
    def arr_right(): return icon("img/arrow1-right.png")

    @staticmethod
    def arr_down(): return icon("img/arrow1-down.png")

    @staticmethod
    def viewer(): return icon("img/photo-camera.png")





