#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

from core import services
from core.services import Format

EXTENSIONS = ['.jpg', '.bmp', '.png', '.gif']


class Resources(object):

    def __init__(self, path_list=list()):
        self.__path_list = path_list
        self.__resource_list = list()
        self.__folder_list = list()
        self.__list__()

    def __list__(self):
        for path in self.__path_list:
            for (dir_path, dir_names, filenames) in os.walk(path):
                for fn in filenames:
                    if os.path.splitext(fn)[1].lower() in EXTENSIONS:
                        self.__resource_list.append(os.path.join(dir_path, fn))
                        if dir_path not in self.__folder_list:
                            self.__folder_list.append(dir_path)

    def path_list(self):
        return list(self.__path_list)

    def resource_list(self):
        return list(self.__resource_list)

    def folder_list(self):
        return list(self.__folder_list)

    def paths_count(self):
        return len(self.__path_list)

    def resource_count(self):
        return len(self.__resource_list)

    def folder_count(self):
        return len(self.__folder_list)

    def to_string(self):
        return "resources: %s  |  folders: %s  |  paths: %s" % (
            Format.decimal(self.resource_count()),
            Format.decimal(self.folder_count()),
            Format.decimal(self.paths_count()))

    def get_resource(self, index):
        if index < 0 or index > self.resource_count() - 1:
            return None
        else:
            return self.__resource_list[index]

    def get_index(self, resource):
        if resource in self.__resource_list:
            return self.__resource_list.index(resource)
        else:
            return -1


class Navigator(object):

    def __init__(self, resources=Resources(), filename=None):
        self.__resources = resources
        self.__size = self.__resources.resource_count()
        self.__history_list = list()
        self.__history_index = 0
        self.__index = -1
        self.__current_file = None
        if filename:
            self.__index = self.__resources.get_index(filename)
            if self.__index > -1:
                self.__current_file = filename
        if self.__current_file is None:
            self.__current_file = self.random_file()
        self.__history_list.append(self.__current_file)

    def current_file(self):
        return self.__current_file

    def index(self):
        return self.__index

    def history_index(self):
        return self.__history_index

    def random_file(self):
        if self.__size > 0:
            self.__index = random.randint(0, self.__size - 1)
            return self.__resources.get_resource(self.__index)
        else:
            return None

    def go_down(self):
        self.__history_index += 1
        if self.__history_index > len(self.__history_list) - 1:
            self.__current_file = self.random_file()
            self.__history_list.append(self.__current_file)
        else:
            self.__current_file = self.__history_list[self.__history_index]
            self.__index = self.__resources.get_index(self.__current_file)
        return self.__current_file

    def go_up(self):
        self.__history_index -= 1
        if self.__history_index < 0:
            self.__history_index = 0
        self.__current_file = self.__history_list[self.__history_index]
        self.__index = self.__resources.get_index(self.__current_file)
        return self.__current_file

    def go_left(self):
        self.__index -= 1
        if self.__index < 0:
            self.__index = 0
        self.__current_file = self.__resources.get_resource(self.__index)
        self.__history_index += 1
        self.__history_list.append(self.__current_file)
        return self.__current_file

    def go_right(self):
        self.__index += 1
        if self.__index > self.__size -1:
            self.__index = self.__size - 1
        self.__current_file = self.__resources.get_resource(self.__index)
        self.__history_index += 1
        self.__history_list.append(self.__current_file)
        return self.__current_file

    def basename(self):
        if self.__current_file is None:
            return None
        else:
            return os.path.basename(self.__current_file)

    def dir_name(self):
        if self.__current_file is None:
            return None
        else:
            return os.path.dirname(self.__current_file)

    def hyperlink(self):
        return "<a href=\"file://%s\">%s</a>" % (self.__current_file, self.basename()[:20])

    def g_image(self):
        return GImage.from_navigator(self)


class GImage(object):

    @staticmethod
    def from_navigator(navigator: Navigator):
        return GImage(navigator.current_file(), navigator.index(), navigator.history_index())

    def __init__(self, filename, index=-1, history_index=-1):
        self.__filename = filename
        self.__index = index
        self.__history_index = history_index

    def filename(self):
        return self.__filename

    def index(self):
        return self.__index

    def history_index(self):
        return self.__history_index

    def basename(self):
        if self.__filename is None:
            return None
        else:
            return os.path.basename(self.__filename)

    def dir_name(self):
        if self.__filename is None:
            return None
        else:
            return os.path.dirname(self.__filename)

    def hyperlink(self, length=0, split=False):
        if length > 0:
            generator = services.chunk_string(self.__filename, length)
            display = "\n".join(list(generator))
        elif split:
            display = "%s %s" % (self.dir_name(), self.basename())
        else:
            display = self.__filename
        return "<a href=\"file://%s\">%s</a>" % (self.__filename, display)


