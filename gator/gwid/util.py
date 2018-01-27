#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

import pkg_resources
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtWidgets import qApp, QApplication

LOG = logging.getLogger(__name__)


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


class GHotKey():

    @staticmethod
    def matches(event: QKeyEvent):
        if event.nativeModifiers() == 1048840:
            return GHotKey.is_meta_sequence(event)

        ctrl = QApplication.instance().ctrl
        if ctrl.last_viewer is not None:
            if event.key() == Qt.Key_Down:
                ctrl.last_viewer.go_file_down()
                return True
            elif event.key() == Qt.Key_Up:
                ctrl.last_viewer.go_file_up()
                return True
            elif event.key() == Qt.Key_Left:
                ctrl.last_viewer.go_file_left()
                return True
            elif event.key() == Qt.Key_Right:
                ctrl.last_viewer.go_file_right()
                return True
            elif event.key() == Qt.Key_G:
                ctrl.last_viewer.activate_main_window()
                return True
        return False

    @staticmethod
    def is_meta_sequence(event: QKeyEvent):
        if event.nativeModifiers() != 1048840:
            return  False
        if event.key() == Qt.Key_X:
            LOG.info("Quiting application")
            qApp.quit()
            return True






