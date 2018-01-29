#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import random

from bdbs.obj import Resource
from bdbs.store import Store
from core import services
from core.services import Format

LOG = logging.getLogger(__name__)

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

    def __init__(self, store: Store, resources=Resources(), filename=None):
        self.__store = store
        self.__resources = resources
        self.__max_views = self.__store.view_date_store().max_views()
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
            self.__current_file = self.__random_file()
        self.__history_list.append(self.__current_file)
        self.__current_resource = self.__create_resource()

    def current_resource(self) -> Resource:
        return self.__current_resource

    def current_file(self):
        return self.__current_file

    def index(self):
        return self.__index

    def history_index(self):
        return self.__history_index

    def __random_file(self):
        if self.__size > 0:
            self.__index = random.randint(0, self.__size - 1)
            filename = self.__resources.get_resource(self.__index)
            views = self.__store.view_date_store().count_views(filename)
            while views >= self.__max_views:
                LOG.debug("%d views >= %d max views for %s" % (views, self.__max_views, filename))
                self.__index += 1
                if self.__index >= self.__size:
                    self.__max_views = self.__store.view_date_store().max_views() + 1
                    self.__index = 0
                filename = self.__resources.get_resource(self.__index)
                views = self.__store.view_date_store().count_views(filename)
            return filename
        else:
            return None

    def go_down(self):
        self.__history_index += 1
        if self.__history_index > len(self.__history_list) - 1:
            self.__current_file = self.__random_file()
            self.__history_list.append(self.__current_file)
        else:
            self.__current_file = self.__history_list[self.__history_index]
            self.__index = self.__resources.get_index(self.__current_file)
        return self.__create_resource()

    def go_up(self):
        self.__history_index -= 1
        if self.__history_index < 0:
            self.__history_index = 0
        self.__current_file = self.__history_list[self.__history_index]
        self.__index = self.__resources.get_index(self.__current_file)
        return self.__create_resource()

    def go_left(self):
        self.__index -= 1
        if self.__index < 0:
            self.__index = 0
        self.__current_file = self.__resources.get_resource(self.__index)
        self.__history_index += 1
        self.__history_list.append(self.__current_file)
        return self.__create_resource()

    def go_right(self):
        self.__index += 1
        if self.__index >= self.__size:
            self.__index = self.__size - 1
        self.__current_file = self.__resources.get_resource(self.__index)
        self.__history_index += 1
        self.__history_list.append(self.__current_file)
        return self.__create_resource()

    def __create_resource(self) -> Resource:
        self.__current_resource = Resource(self.__current_file, self.__index, self.__history_index)
        self.__store.view_date_store().update(self.__current_resource)
        return self.__current_resource

