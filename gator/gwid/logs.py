#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os
import sys


def switch_logging(log_filename):
    log_dir = os.path.dirname(log_filename)
    os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s - %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]")

    file_handler = logging.handlers.RotatingFileHandler(filename=log_filename, maxBytes=1000000, backupCount=3)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)

    root_logger = logging.getLogger()  # root logger

    for handler in root_logger.handlers[:]:  # remove all old handlers
        root_logger.removeHandler(handler)

    root_logger.addHandler(file_handler)  # set the new handler
    root_logger.addHandler(stdout_handler)
    LOG = logging.getLogger(__name__)
    LOG.info("Switched logging       : %s" % log_filename)
    LOG.info("\n"
                "     _____    ___________   ______   ______\n"
                "    / ___/   /   ___  ___| / __   | / __  |\n"
                "   / / _    / _  |  | |   / /  / / / /_/ / \n"
                "  / / | |  / /_| |  | |  / /  / / /  _  |  \n"
                " / /__| | / ___  |  | | / /__/ / /  / | |  \n"
                " |______//_/   |_|  |_| |_____/ /__/  |_|  \n\n")