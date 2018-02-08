#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtWidgets import qApp, QApplication

LOG = logging.getLogger(__name__)
ROOT = os.path.dirname(os.path.abspath(__name__)) if os.path.exists(
    os.path.join(os.path.dirname(os.path.abspath(__name__)), "img")) else os.path.dirname(
    os.path.dirname(os.path.abspath(__name__)))
LOG.info("ROOT: %s" % ROOT)


def icon(filename):
    path = os.path.join(ROOT, "img", filename)
    if not os.path.exists(path):
        LOG.warning("File not found: %s" % path)
    return QIcon(path)


class GIcon(object):

    @staticmethod
    def plus(): return icon("plus-sign.png")

    @staticmethod
    def minus(): return icon("minus.png")

    @staticmethod
    def arr2_up(): return icon("arrow2-up.png")

    @staticmethod
    def arr2_down(): return icon("arrow2-down.png")

    @staticmethod
    def arr_left(): return icon("arrow1-left.png")

    @staticmethod
    def arr_up(): return icon("arrow1-up.png")

    @staticmethod
    def arr_right(): return icon("arrow1-right.png")

    @staticmethod
    def arr_down(): return icon("arrow1-down.png")

    @staticmethod
    def viewer(): return icon("photo-camera.png")


class GHotKey():

    @staticmethod
    def matches(event: QKeyEvent):
        if event.nativeModifiers() == 1048840:
            return GHotKey.is_meta_sequence(event)
        elif event.key() == Qt.Key_X:
            LOG.info("Quiting application")
            qApp.quit()
            return True

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
            elif event.key() == Qt.Key_Backspace:
                ctrl.last_viewer.go_file_start()
            elif event.key() == Qt.Key_G:
                ctrl.last_viewer.activate_main_window()
                return True
        return False

    @staticmethod
    def is_meta_sequence(event: QKeyEvent):
        if event.nativeModifiers() != 1048840:
            return  False
        # if event.key() == Qt.Key_X:
        #     LOG.info("Quiting application")
        #     qApp.quit()
        #     return True






