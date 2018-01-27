#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.handlers
import os
from inspect import stack, FrameInfo

import gwid.logs
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from core import services
from core.configuration import GatorConf, PathFinder
from core.navigator import Resources

LOG = logging.getLogger(__name__)


class Ctrl(QObject):

    sgn_main_window_closing = pyqtSignal()
    sgn_switch_configuration = pyqtSignal()
    sgn_switch_resources = pyqtSignal()

    def __init__(self, gator_config: GatorConf):
        QObject.__init__(self)
        self.path_finder = PathFinder()
        self.config = gator_config
        self.configuration_file = self.config.config_file()
        self.gator_home = os.path.dirname(self.configuration_file)
        self.configuration_index = self.path_finder.index(self.configuration_file)
        LOG.info("Configuration: %s" % self.configuration_file)
        LOG.info("Gator Home   : %s" % self.gator_home)
        self.resources = Resources(self.config.resources())
        LOG.info(self.resources.to_string())

    def close(self):
        LOG.info("Closing Ctrl")
        self.sgn_main_window_closing.emit()

    def switch_configuration(self, configuration_file: str):
        if self.configuration_file == configuration_file:
            return
        LOG.info("Switching configuration: %s" % configuration_file)
        self.configuration_file = os.path.abspath(configuration_file)
        self.gator_home = os.path.dirname(self.configuration_file)
        self.config = GatorConf(self.configuration_file)
        self.config.set_log_file(os.path.join(os.path.dirname(self.configuration_file), "logs", "gator.log"))
        gwid.logs.switch_logging(self.config.log_file())
        self.config.persist()

        self.path_finder.insert_conditionally(0, self.configuration_file)
        self.configuration_index = self.path_finder.index(self.configuration_file)

        self.sgn_switch_configuration.emit()
        LOG.info("Switched configuration : %s" % self.configuration_file)
        LOG.info("Gator Home             : %s" % self.gator_home)
        self.switch_resources()

    def switch_resources(self):
        self.resources = Resources(self.config.resources())
        LOG.info(self.resources.to_string())
        self.sgn_switch_resources.emit()

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
        return "\n".join([Ctrl.__msg_detail(f) for f in frame_stack[3:]])







