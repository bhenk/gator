#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import sys

import pkg_resources
from PyQt5.QtGui import QIcon

ICON_ARROW_DOWN = "img/arrow1-down.png"
ICON_ARROW_LEFT = "img/arrow1-left.png"
ICON_ARROW_UP = "img/arrow1-up.png"
ICON_ARROW_RIGHT = "img/arrow1-right.png"


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def icon(filename):
    path = pkg_resources.resource_filename(__name__, filename)
    return QIcon(path)


def switch_logging(log_filename):
    log_dir = os.path.dirname(log_filename)
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]")

    file_handler = logging.handlers.RotatingFileHandler(filename=log_filename, maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)

    log = logging.getLogger()  # root logger

    for handler in log.handlers[:]:  # remove all old handlers
        log.removeHandler(handler)

    log.addHandler(file_handler)  # set the new handler
    log.addHandler(stdout_handler)
    logger = logging.getLogger(__name__)
    logger.info("Switched logging       : %s" % log_filename)
    logger.info("\n"
                "     _____    ___________   ______   ______\n"
                "    / ___/   /   ___  ___| / __   | / __  |\n"
                "   / / _    / _  |  | |   / /  / / / /_/ / \n"
                "  / / | |  / /_| |  | |  / /  / / /  _  |  \n"
                " / /__| | / ___  |  | | / /__/ / /  / | |  \n"
                " |______//_/   |_|  |_| |_____/ /__/  |_|  \n\n")
