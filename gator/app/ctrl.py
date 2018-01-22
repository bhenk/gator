#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

import sys
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox
from core.configuration import GatorConf, PathFinder

LOG = logging.getLogger(__name__)


class Ctrl(QObject):

    sgn_main_window_closing = pyqtSignal()
    sgn_switch_configuration = pyqtSignal()

    def __init__(self, application_home, gator_config: GatorConf):
        QObject.__init__(self)
        self.application_home = application_home
        self.path_finder = PathFinder()
        self.config = gator_config
        self.configuration_file = self.config.config_file
        if self.configuration_file is not None and  os.path.exists(self.configuration_file):
            self.gator_home = os.path.dirname(self.configuration_file)
        else:
            self.gator_home = None
        self.configuration_index = -1

    def close(self):
        LOG.info("Closing Ctrl")
        self.sgn_main_window_closing.emit()

    def abs_path(self, filename):
        return os.path.join(self.application_home, filename)

    def img_path(self, filename):
        return os.path.join(self.application_home, "conf", "img", filename)

    def icon(self, filename):
        return QIcon(self.img_path(filename))

    def switch_configuration(self, configuration_file: str):
        home = os.path.dirname(os.path.abspath(configuration_file))
        if not os.path.exists(home):
            self.warn("Gator Home does not exist: %s" % home)
            home = self.path_finder.first_existing_dir()
            if home is None:
                return
            configuration_file = os.path.join(home, "gator.cfg")
        LOG.info("Switching configuration: %s" % configuration_file)
        self.configuration_file = os.path.abspath(configuration_file)
        self.configuration_index = self.path_finder.index(self.configuration_file)
        self.gator_home = os.path.dirname(self.configuration_file)
        log_dir = os.path.join(self.gator_home, "logs")
        os.makedirs(log_dir, exist_ok=True)

        self.config = GatorConf(self.configuration_file)
        self.config.set_log_file(os.path.join(log_dir, "gator.log"))
        self.switch_logging()
        self.sgn_switch_configuration.emit()
        LOG.info("Switched configuration : %s" % self.configuration_file)
        LOG.info("Gator Home             : %s" % self.gator_home)

    def switch_logging(self):
        file_handler = logging.FileHandler(self.config.log_file())
        log = logging.getLogger()  # root logger
        formatter = logging.Formatter("%(asctime)s - %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]")
        file_handler.setFormatter(formatter)

        stdout_handler = logging.StreamHandler(stream=sys.stdout)
        stdout_handler.setFormatter(formatter)

        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        log.addHandler(file_handler)  # set the new handler
        LOG.info("\n"
                    "     _____    ___________   ______   ______\n"
                    "    / ___/   /   ___  ___| / __   | / __  |\n"
                    "   / / _    / _  |  | |   / /  / / / /_/ / \n"
                    "  / / | |  / /_| |  | |  / /  / / /  _  |  \n"
                    " / /__| | / ___  |  | | / /__/ / /  / | |  \n"
                    " |______//_/   |_|  |_| |_____/ /__/  |_|  \n\n")
        log.addHandler(stdout_handler)
        LOG.info("Switched logging       : %s" % self.config.log_file())

    @staticmethod
    def error(msg, cause=None):
        LOG.exception(msg, exc_info=cause)
        Ctrl.__msg(QMessageBox.Critical, msg, cause)

    @staticmethod
    def warn(msg, cause=None):
        LOG.warning(msg, exc_info=cause)
        Ctrl.__msg(QMessageBox.Warning, msg, cause)

    @staticmethod
    def __msg(icon, text, cause=None):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Gator")
        if cause:
            msg_box.setText("%s\nCaused by:\n\n%s") % (text, cause)
        else:
            msg_box.setText(text)
        msg_box.setIcon(icon)
        msg_box.exec()



