#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import core.services as serv

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent
from PyQt5.QtWidgets import qApp, QApplication

LOG = logging.getLogger(__name__)
# ROOT = os.path.dirname(os.path.abspath(__name__)) if os.path.exists(
#     os.path.join(os.path.dirname(os.path.abspath(__name__)), "img")) else os.path.dirname(
#     os.path.dirname(os.path.abspath(__name__)))
ROOT = serv.application_home()
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
    def open_file(): return icon("view-files.png")

    @staticmethod
    def close_view(): return icon("window-close.png")

    @staticmethod
    def close_views(): return icon("windows-close.png")

    @staticmethod
    def exit(): return icon("exit.png")

    @staticmethod
    def acme(): return icon("snowy-mountains.png")

    @staticmethod
    def copy_image(): return icon("security-copy.png")

    @staticmethod
    def copy_filename(): return icon("copy-filename.png")

    @staticmethod
    def configuration(): return icon("wrench.png")

    @staticmethod
    def universe(): return icon("open-folder.png")

    @staticmethod
    def viewer(): return icon("open-eye-black.png")

    @staticmethod
    def viewer_white(): return icon("open-eye.png")

    @staticmethod
    def gator(): return icon("chinese-door.png")

    @staticmethod
    def arrow_white_up(): return icon("arrow_small_w_up.png")

    @staticmethod
    def arrow_white_left(): return icon("arrow_small_w_left.png")

    @staticmethod
    def arrow_white_right(): return icon("arrow_small_w_right.png")

    @staticmethod
    def arrow_white_down(): return icon("arrow_small_w_down.png")

    @staticmethod
    def zero_white(): return icon("zero.png")

    @staticmethod
    def history_start(): return icon("arrow_end_up.png")

    @staticmethod
    def history_end(): return icon("arrow_end_down.png")


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






