#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QTabWidget
from app.ctrl import Ctrl
from app.gframe import GFrame
from app.tconfig import ConfigureFrame
from app.tview import ViewFrame

LOG = logging.getLogger(__name__)


# ################################################################
class Gator(QApplication):

    def __init__(self, *args, application_home=None, gator_config=None):
        QApplication.__init__(self, *args)
        self.ctrl = Ctrl(application_home, gator_config)

        LOG.info("Start Gator. application_home: %s" % self.ctrl.application_home)

        self.main_window = WMain()
        self.aboutToQuit.connect(self.__before_close__)

    def __before_close__(self):
        LOG.info("Closing Gator")
        self.main_window.close()
        LOG.info("Closed Gator")


# ################################################################
class WMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ctrl = QApplication.instance().ctrl
        self.setWindowTitle("Gator")
        self.create_menus()
        self.tabframe = TabbedFrame(self)
        self.setCentralWidget(self.tabframe)
        self.resize(self.ctrl.config.main_window_width(), self.ctrl.config.main_window_height())

    def create_menus(self):
        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)

        self.menu_file = QMenu("File", self)
        self.menubar.addMenu(self.menu_file)

    def close(self):
        LOG.debug("Main window is closing")
        self.ctrl.config.set_main_window_height(self.height())
        self.ctrl.config.set_main_window_width(self.width())
        self.ctrl.config.persist()

    def closeEvent(self, event: QCloseEvent):
        self.ctrl.close()
        event.accept()


# ################################################################
class TabbedFrame(QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.previndex = -1
        self.init_ui()

    def init_ui(self):
        self.gframe = GFrame(self)
        self.frame_view = ViewFrame(self, 0)
        self.frame_configure = ConfigureFrame(self, 1)

        self.addTab(self.gframe, "Main")
        self.addTab(self.frame_view, "View")
        self.addTab(self.frame_configure, "Configure")
