#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.handlers
import os
from inspect import stack, FrameInfo

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QMenu, QMenuBar

import gwid.logs
from app.menu import GMenuBar
from bdbs.obj import Resource
from bdbs.store import Store
from core import services
from core.configuration import GatorConf, PathFinder
from core.navigator import Resources

LOG = logging.getLogger(__name__)


class Ctrl(QObject):

    sgn_main_window_closing = pyqtSignal()
    sgn_switch_configuration = pyqtSignal()
    sgn_switch_resources = pyqtSignal()
    sgn_resource_changed = pyqtSignal(Resource)

    def __init__(self, gator_config: GatorConf):
        QObject.__init__(self)
        self.path_finder = PathFinder()
        self.config = gator_config  # type: GatorConf
        self.configuration_file = self.config.config_file()
        self.gator_home = os.path.dirname(self.configuration_file)
        self.configuration_index = self.path_finder.index(self.configuration_file)
        LOG.info("Configuration: %s" % self.configuration_file)
        LOG.info("Gator Home   : %s" % self.gator_home)

        self.resources = Resources(self.config.resources())
        LOG.info(self.resources.to_string())
        db_home = os.path.join(self.gator_home, "db")
        self.store = Store(db_home)
        LOG.info("Gator store  : %s" % self.store.repository.db_home())

        self.last_viewer = None
        self.is_closing = False
        self.__menu_bar = GMenuBar()
        self.__menu_bar.setNativeMenuBar(True)

    def menu_bar(self) -> QMenuBar:
        """
        Handle for the common menu bar.
        :return: The menu bar.
        :rtype : QMenuBar
        """
        return self.__menu_bar

    def menu_file(self) -> QMenu:
        """
        Handle for the `File` menu.
        :return: The `File` menu.
        :rtype : QMenu
        """
        return self.__menu_bar.menu_file

    def menu_view(self) -> QMenu:
        """
        Handle for the `View` menu.
        :return: The `View` menu.
        @rtype : QMenu
        """
        return self.__menu_bar.menu_view

    def menu_edit(self) -> QMenu:
        """
        Handle for the `Edit` menu.
        :return: The `Edit` menu.
        @rtype : QMenu
        """
        return self.__menu_bar.menu_edit

    def menu_window(self) -> QMenu:
        """
        Handle for the `Window` menu.
        :return: The `Window` menu.
        @rtype : QMenu
        """
        return self.__menu_bar.menu_window

    def menu_close_viewer(self) -> QMenu:
        """
        A submenu on the `File` menu.
        :return: submenu on the `File` menu
        @rtype : QMenu
        """
        return self.__menu_bar.menu_close_viewer

    def close(self):
        self.store.close()
        if not self.is_closing:
            self.is_closing = True
            LOG.info("Closing Ctrl")
            self.sgn_main_window_closing.emit()

    def switch_configuration(self, configuration_file: str):
        if self.configuration_file == configuration_file:
            return
        LOG.info("Switching configuration: %s" % configuration_file)
        self.store.close()
        self.config.persist()

        self.configuration_file = os.path.abspath(configuration_file)
        self.gator_home = os.path.dirname(self.configuration_file)
        self.config = GatorConf(self.configuration_file)
        self.config.set_log_file(os.path.join(os.path.dirname(self.configuration_file), "logs", "gator.log"))
        gwid.logs.switch_logging(self.config.log_file())
        self.config.persist()

        self.path_finder.insert_conditionally(0, self.configuration_file)
        self.configuration_index = self.path_finder.index(self.configuration_file)

        db_home = os.path.join(self.gator_home, "db")
        self.store = Store(db_home)

        self.sgn_switch_configuration.emit()
        LOG.info("Switched configuration : %s" % self.configuration_file)
        LOG.info("Gator Home             : %s" % self.gator_home)
        LOG.info("Gator store            : %s" % self.store.repository.db_home())
        self.switch_resources()

    def switch_resources(self):
        self.resources = Resources(self.config.resources())
        LOG.info(self.resources.to_string())
        self.sgn_switch_resources.emit()

    def set_last_viewer(self, viewer):
        self.last_viewer = viewer

    @staticmethod
    def error(msg, cause=None):
        LOG.exception(msg, exc_info=cause)
        Ctrl.__msg(QMessageBox.Critical, msg, cause)

    @staticmethod
    def warn(msg, cause=None):
        LOG.warning(msg, exc_info=cause)
        Ctrl.__msg(QMessageBox.Warning, msg, cause)

    @staticmethod
    def info(msg):
        LOG.info(msg)
        Ctrl.__msg(QMessageBox.Information, msg, None)

    @staticmethod
    def __msg(icon, text, cause=None):
        frame_stack = stack()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Gator")
        if cause:
            cs = "\nCaused by:\n\n%s" % cause
        else:
            cs = ""
        msg_box.setText("%s%s" % (text, cs))
        msg_box.setInformativeText(Ctrl.__msg_detail(frame_stack[3]))
        msg_box.setDetailedText(Ctrl.__msg_details(frame_stack))
        msg_box.setIcon(icon)
        msg_box.exec()

    @staticmethod
    def __msg_detail(frame_info):
        f_name = os.path.relpath(frame_info.filename, services.application_home()).replace("/", ".")
        return "[%s:%d] %s" % (f_name, frame_info.lineno, frame_info.function)

    @staticmethod
    def __msg_details(frame_stack: FrameInfo):
        return "\n".join([Ctrl.__msg_detail(f) for f in frame_stack])







