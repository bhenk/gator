#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtGui import QCloseEvent, QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu

from app.ctrl import Ctrl
from app.gframe import GFrame
from gwid.util import GHotKey

LOG = logging.getLogger(__name__)


# ################################################################
class Gator(QApplication):

    def __init__(self, *args, gator_config=None):
        QApplication.__init__(self, *args)
        LOG.info("Gator started")
        self.ctrl = Ctrl(gator_config)

        self.main_window = WMain()
        #self.main_window = GMainWindow()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
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

        self.gframe = GFrame(self)
        self.setCentralWidget(self.gframe)
        self.move(self.ctrl.config.main_window_x(), self.ctrl.config.main_window_y())

    def keyPressEvent(self, event: QKeyEvent):
        if GHotKey.matches(event):
            return

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


