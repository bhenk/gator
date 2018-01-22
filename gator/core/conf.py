#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

import os
import platform
from configparser import ConfigParser

CFG_FILENAME = "gator.cfg"
CFG_DIRNAME = "gator"
SECTION_CORE = "core"
SECTION_WINDOW = "window"

LOG = logging.getLogger(__name__)


class Configuration(object):
    """
    :samp:`Singleton persisting object for storing configuration parameters`

    """

    _configuration_filename = CFG_FILENAME

    @staticmethod
    def _set_configuration_filename(cfg_filename):
        LOG.info("Setting Conf filename to %s", cfg_filename)
        Configuration._configuration_filename = cfg_filename

    @staticmethod
    def _get_configuration_filename():
        if not Configuration._configuration_filename:
            Configuration._set_configuration_filename(CFG_FILENAME)

        return Configuration._configuration_filename

    @staticmethod
    def reset():
        Configuration._instance = None
        LOG.info("Conf was reset.")

    @staticmethod
    def _get_config_path():
        c_path = os.path.expanduser("~")
        opsys = platform.system()
        if opsys == "Windows":
            win_path = os.path.join(c_path, "AppData", "Local")
            if os.path.exists(win_path): c_path = win_path
        elif opsys == "Darwin":
            dar_path = os.path.join(c_path, ".config")
            if not os.path.exists(dar_path): os.makedirs(dar_path)
            if os.path.exists(dar_path): c_path = dar_path
        elif opsys == "Linux":
            lin_path = os.path.join(c_path, ".config")
            if not os.path.exists(lin_path): os.makedirs(lin_path)
            if os.path.exists(lin_path): c_path = lin_path

        c_path = os.path.join(c_path, CFG_DIRNAME, "conf")
        if not os.path.exists(c_path):
            os.makedirs(c_path)
        LOG.info("Configuration directory: %s", c_path)
        return c_path

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # LOG.info("Creating Configuration._instance")
            cls._instance = super(Configuration, cls).__new__(cls, *args)
            cls.config_path = cls._get_config_path()
            cls.config_file = os.path.join(cls.config_path, Configuration._get_configuration_filename())
            cls.parser = ConfigParser()
            if os.path.exists(cls.config_file):
                cls.parser.read(cls.config_file)
        return cls._instance

    def config_path(self):
        return self.config_path

    def config_file(self):
        return self.config_file

    def name(self):
        return os.path.splitext(os.path.basename(self.config_file))[0]

    def persist(self):
        f = open(self.config_file, "w")
        self.parser.write(f)
        f.close()
        LOG.info("Persisted GuiConf as %s", self.config_file)

    def __set_option__(self, section, option, value):
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        if value is None:
            self.parser.remove_option(section, option)
        else:
            self.parser.set(section, option, value)

    def __get_int__(self, section, option, fallback=0):
        value = self.parser.get(section, option, fallback=str(fallback))
        return int(value)

    def __set_int__(self, section, option, value):
        self.__set_option__(section, option, str(value))

    def __get_boolean__(self, section, option, fallback=True):
        value = self.parser.get(section, option, fallback=str(fallback))
        return not(value == "False" or value == "None")

    def __set_boolean__(self, section, option, value):
        self.__set_option__(section, option, str(value))

    def __get_list__(self, section, option, fallback=list()):
        value = self.parser.get(section, option, fallback="\n".join(fallback))
        if value == "":
            return []
        else:
            return value.split("\n")

    def __set_list__(self, section, option, value):
        self.__set_option__(section, option, "\n".join(value))

    #####################################################
    # SECTION CORE
    def resource_dir(self, fallback=os.path.expanduser("~")):
        return self.parser.get(SECTION_CORE, "resource_dir", fallback=fallback)

    def set_resource_dir(self, resource_dir):
        self.__set_option__(SECTION_CORE, "resource_dir", resource_dir)

    #####################################################
    # SECTION_WINDOW
    def window_width(self, fallback=500):
        return self.__get_int__(SECTION_WINDOW, "window_width", fallback=fallback)

    def set_window_width(self, width):
        self.__set_int__(SECTION_WINDOW, "window_width", width)

    def window_height(self, fallback=300):
        return self.__get_int__(SECTION_WINDOW, "window_height", fallback=fallback)

    def set_window_height(self, height):
        self.__set_int__(SECTION_WINDOW, "window_height", height)