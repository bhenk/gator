#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
from configparser import ConfigParser

INIT_CFG_DIR_NAME = "gator"


def find_config_dir(dir_name="conf"):
    config_dir = os.path.expanduser("~")
    op_sys = platform.system()
    if op_sys == "Windows":
        win_path = os.path.join(config_dir, "AppData", "Local")
        if os.path.exists(win_path): config_dir = win_path
    elif op_sys == "Darwin":
        dar_path = os.path.join(config_dir, ".config")
        if not os.path.exists(dar_path): os.makedirs(dar_path)
        if os.path.exists(dar_path): config_dir = dar_path
    elif op_sys == "Linux":
        lin_path = os.path.join(config_dir, ".config")
        if not os.path.exists(lin_path): os.makedirs(lin_path)
        if os.path.exists(lin_path): config_dir = lin_path

    config_dir = os.path.join(config_dir, INIT_CFG_DIR_NAME, dir_name)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir


class PathFinder(object):

    def __init__(self, dir_name="init", file_name="paths.txt"):
        self.config_dir = find_config_dir(dir_name)
        self.config_file = os.path.join(self.config_dir, file_name)
        self.__path_list = []
        self.read()

    def read(self):
        if os.path.exists(self.config_file):
            with open(self.config_file) as pf:
                self.__path_list = pf.read().splitlines()

    def persist(self):
        with open(self.config_file, "w") as pf:
            for path in self.__path_list:
                pf.write("%s\n" % path)

    def path_list(self):
        return self.__path_list

    def set_path_list(self, path_list: list):
        self.__path_list = path_list

    def append(self, path):
        self.__path_list.append(path)

    def existing_files(self):
        return [f for f in self.__path_list if os.path.exists(f) and os.path.isfile(f)]

    def existing_dirs(self):
        return [os.path.dirname(f) for f in self.__path_list if os.path.exists(os.path.dirname(f))]

    def first_existing_dir(self):
        existing_dirs = self.existing_dirs()
        if len(existing_dirs) == 0:
            return None
        else:
            return existing_dirs[0]

    def first_existing_file(self):
        existing_files = self.existing_files()
        if len(existing_files) == 0:
            return None
        else:
            return existing_files[0]

    def index(self, configuration_file):
        return self.__path_list.index(configuration_file)


class Configuration(object):

    def __init__(self, config_file=None):
        self.config_file = config_file
        self.parser = ConfigParser()
        self.read()

    def read(self):
        if self.config_file is not None and os.path.exists(self.config_file):
            self.parser.read(self.config_file)
            return True
        else:
            return False

    def persist(self):
        if self.config_file is not None and os.path.exists(self.config_file):
            with open(self.config_file, "w") as cf:
                self.parser.write(cf)
            return True
        else:
            return False

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


class GatorConf(Configuration):
    SECTION_CORE = "core"
    SECTION_WINDOW = "window"

    def __init__(self, config_file=None):
        Configuration.__init__(self, config_file)
        config_dir = find_config_dir("init")
        self.default_log_file = os.path.join(config_dir, "gator.log")


    #####################################################
    # SECTION CORE
    def log_file(self):
        return self.parser.get(GatorConf.SECTION_CORE, "log_file", fallback=self.default_log_file)

    def set_log_file(self, log_file):
        self.__set_option__(GatorConf.SECTION_CORE, "log_file", log_file)

    def resource_dir(self, fallback=os.path.expanduser("~/tmp")):
        return self.parser.get(GatorConf.SECTION_CORE, "resource_dir", fallback=fallback)

    def set_resource_dir(self, resource_dir):
        self.__set_option__(GatorConf.SECTION_CORE, "resource_dir", resource_dir)

    #####################################################
    # SECTION_WINDOW
    def main_window_width(self, fallback=500):
        return self.__get_int__(GatorConf.SECTION_WINDOW, "main_window_width", fallback=fallback)

    def set_main_window_width(self, width):
        self.__set_int__(GatorConf.SECTION_WINDOW, "main_window_width", width)

    def main_window_height(self, fallback=300):
        return self.__get_int__(GatorConf.SECTION_WINDOW, "main_window_height", fallback=fallback)

    def set_main_window_height(self, height):
        self.__set_int__(GatorConf.SECTION_WINDOW, "main_window_height", height)


