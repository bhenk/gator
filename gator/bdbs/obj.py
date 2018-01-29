#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


class Resource(object):

    def __init__(self, filename, index=-1, history_index=-1):
        self.__filename = filename
        self.__index = index
        self.__history_index = history_index
        self.__view_dates = list()

    def filename(self):
        return self.__filename

    def index(self):
        return self.__index

    def history_index(self):
        return self.__history_index

    def has_file(self):
        return self.__filename is not None

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

    def hyperlink(self, length=0, split=False, basename=False):
        if length > 0:
            generator = chunk_string(self.__filename, length)
            display = "\n".join(list(generator))
        elif split:
            display = "%s %s" % (self.dir_name(), self.basename())
        elif basename:
            display = self.basename()
        else:
            display = self.__filename
        return "<a href=\"file://%s\">%s</a>" % (self.__filename, display)

    def set_view_dates(self, view_dates: list()):
        self.__view_dates = view_dates

    def view_dates(self, fmt=None):
        if fmt:
            return [dt.strftime(fmt) for dt in self.__view_dates]
        return self.__view_dates

    def view_dates_as_string(self):
        return " | ".join(self.view_dates("%Y-%m-%d %H:%M:%S"))

    def count_view_dates(self):
        return len(self.__view_dates)
