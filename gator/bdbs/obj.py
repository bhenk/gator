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
        self.__acme_dates = list()

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

    def short_name(self):
        if self.__filename is None:
            return None
        else:
            return os.path.splitext(self.basename())[0]

    def long_name(self):
        return "%s %s" % (self.short_name(), self.slv_index())

    def hyperlink(self, length=0, split=False, basename=False, slv_index=False):
        if length > 0:
            generator = chunk_string(self.__filename, length)
            display = "\n".join(list(generator))
        elif split:
            display = "%s %s" % (self.dir_name(), self.basename())
        elif basename:
            display = self.basename()
        elif slv_index:
            display = self.slv_index()
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
        return "\n".join(self.view_dates("%Y-%m-%d %H:%M:%S"))

    def count_view_dates(self):
        return len(self.__view_dates)

    def set_acme_dates(self, acme_dates: list()):
        self.__acme_dates = acme_dates

    def acme_dates(self, fmt=None):
        if fmt:
            return [dt.strftime(fmt) for dt in self.__acme_dates]
        return self.__acme_dates

    def acm_dates_as_string(self):
        return "\n".join(self.acme_dates("%Y-%m-%d %H:%M:%S"))

    def count_acme_dates(self):
        return len(self.__acme_dates)

    def slv_index(self):
        return "sl# %s" % str(self.__index).zfill(6)