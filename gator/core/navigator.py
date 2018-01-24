#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

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

    def __init__(self, resources=Resources()):
        self.resources = resources
        self.__size = self.resources.resource_count()
        self.history_list = list()
        self.history_pointer = 0
        self.index = -1
        self.current_file = self.random_file()
        self.history_list.append(self.current_file)

    def random_file(self):
        if self.__size > 0:
            self.index = random.randint(0, self.__size - 1)
            return self.resources.get_resource(self.index)
        else:
            return None

    def go_down(self):
        self.history_pointer += 1
        if self.history_pointer > len(self.history_list) - 1:
            self.current_file = self.random_file()
            self.history_list.append(self.current_file)
        else:
            self.current_file = self.history_list[self.history_pointer]
            self.index = self.resources.get_index(self.current_file)
        return self.current_file

    def go_up(self):
        self.history_pointer -= 1
        if self.history_pointer < 0:
            self.history_pointer = 0
        self.current_file = self.history_list[self.history_pointer]
        self.index = self.resources.get_index(self.current_file)
        return self.current_file

    def go_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = -1
        self.current_file = self.resources.get_resource(self.index)
        self.history_pointer += 1
        self.history_list.append(self.current_file)
        return self.current_file

    def go_right(self):
        self.index += 1
        if self.index > self.__size -1:
            self.index = self.__size -1
        self.current_file = self.resources.get_resource(self.index)
        self.history_pointer += 1
        self.history_list.append(self.current_file)
        return self.current_file

    def filename(self):
        if self.current_file is None:
            return None
        else:
            return os.path.basename(self.current_file)

    def dir_name(self):
        if self.current_file is None:
            return None
        else:
            return os.path.dirname(self.current_file)
