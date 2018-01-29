#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


class Format(object):

    @staticmethod
    def decimal(number=0):
        return "{0:,g}".format(number).replace(",", ".")
