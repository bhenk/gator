#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Format(object):

    @staticmethod
    def decimal(number=0):
        return "{0:,g}".format(number).replace(",", ".")