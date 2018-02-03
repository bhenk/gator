#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config
import os
import sys

CONFIGURATION_DIR = "conf"
LOGGING_CFG_FILE = "logging.conf"


if __name__ == '__main__':
    #locale.setlocale(locale.LC_ALL, 'nl_NL')

    if getattr(sys, 'frozen', False):
        # running in a bundle
        application_home = sys._MEIPASS
    else:
        application_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    # Start this module from anywhere on the system: append root directory of project.
    sys.path.append(application_home)

    from core.configuration import PathFinder, GatorConf

    # Find out some initial paths
    path_finder = PathFinder()
    config_file = path_finder.first_existing_file()
    gator_config = GatorConf(config_file)

    # initialize logging
    log_file = gator_config.log_file()
    log_dir = os.path.dirname(log_file)
    os.makedirs(log_dir, exist_ok=True)
    # For Windows single backslash path names:
    log_file = log_file.replace("\\", "\\\\")
    # configure logging
    log_conf = os.path.join(application_home, CONFIGURATION_DIR, LOGGING_CFG_FILE)
    logging.config.fileConfig(log_conf, defaults={"log_file": log_file})
    # create a logger
    logger = logging.getLogger(__name__)
    logger.info("Initialized logging: %s" % log_file)
    logger.info("\n"
    "     _____    ___________   ______   ______\n"
    "    / ___/   /   ___  ___| / __   | / __  |\n"
    "   / / _    / _  |  | |   / /  / / / /_/ / \n"
    "  / / | |  / /_| |  | |  / /  / / /  _  |  \n"
    " / /__| | / ___  |  | | / /__/ / /  / | |  \n"
    " |______//_/   |_|  |_| |_____/ /__/  |_|  \n\n")

    logger.info("home: %s" % application_home)

    # create the application
    from app.gator import Gator
    application = Gator(sys.argv, gator_config=gator_config)

    # start the application
    application.main_window.show()
    sys.exit(application.exec_())