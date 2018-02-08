#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QWidget

import version
from app.ctrl import Ctrl
from app.gframe import GFrame
from gwid.util import GHotKey

LOG = logging.getLogger(__name__)


# ################################################################
class Gator(QApplication):

    def __init__(self, *args, gator_config=None):
        QApplication.__init__(self, *args)
        LOG.info("Gator version = %s | release date: %s" % (version.__version__, version.__release_date__))
        self.ctrl = Ctrl(gator_config)

        self.main_window = WMain()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
        """
        Give child widgets a chance to clean up.
        """
        LOG.info("Closing Gator")
        self.main_window.close()
        LOG.info("Gator closed")


# ################################################################
class WMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gator")
        self.ctrl = QApplication.instance().ctrl

        self.setMenuBar(self.ctrl.menu_bar())
        self.menu_file = self.ctrl.menu_file()  # type: QMenu

        action_exit = QAction("3&xit Gator", self)
        action_exit.setShortcut("Ctrl+X")
        action_exit.triggered.connect(QApplication.quit)
        self.ctrl.menu_file().addAction(action_exit)

        self.action_activate_me = QAction("Gator", self)
        self.action_activate_me.triggered.connect(self.activate_self)
        self.action_activate_me.setCheckable(True)
        self.ctrl.menu_window().addAction(self.action_activate_me)

        self.gframe = GFrame(self)
        self.setCentralWidget(self.gframe)
        self.move(self.ctrl.config.main_window_x(), self.ctrl.config.main_window_y())

    def keyPressEvent(self, event: QKeyEvent):
        if GHotKey.matches(event):
            return

    def activate_self(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def event(self, event: QEvent):
        if event.type() == QEvent.WindowActivate:
            self.action_activate_me.setChecked(True)
            return True
        elif event.type() == QEvent.WindowDeactivate:
            self.action_activate_me.setChecked(False)
            return True
        return QWidget.event(self, event)

    def close(self):
        LOG.debug("Main window is closing")
        self.ctrl.close()
        self.ctrl.config.set_main_window_height(self.height())
        self.ctrl.config.set_main_window_width(self.width())
        self.ctrl.config.set_main_window_x(self.pos().x())
        self.ctrl.config.set_main_window_y(self.pos().y())
        LOG.debug("##### Persist configuration @ %s" % self.ctrl.config.config_file())
        self.ctrl.config.persist()

    def closeEvent(self, event: QCloseEvent):
        LOG.debug("Main window close event")
        QApplication.quit()
        event.accept()


