#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os
import sys
from statistics import mean, harmonic_mean, median, median_low, median_high, stdev, pstdev


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        try:
            _app_home = sys._MEIPASS
        except Exception as err:
            _app_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    else:
        _app_home = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return  _app_home


def chunk_string(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))


class Format(object):

    DATE_FULL = "%Y-%m-%d %H:%M:%S"
    DAY = "%Y-%m-%d"

    @staticmethod
    def decimal(number=0):
        return "{0:,g}".format(number).replace(",", ".")


class Stat(object):

    def __init__(self, sequence):
        self.__sequence = sequence
        self.__len_seq = len(self.__sequence)
        empty = self.__len_seq == 0
        self.__min = 0 if empty else min(self.__sequence)
        self.__len_min = len([x for x in self.__sequence if x == self.__min])
        self.__max = 0 if empty else max(self.__sequence)
        self.__len_max = len([x for x in self.__sequence if x == self.__max])
        self.__mean = 0 if empty else mean(self.__sequence)
        self.__median = 0 if empty else median(self.__sequence)
        self.__stdev = -1 if len(self.__sequence) < 2 else stdev(self.__sequence)

    def len_seq(self):
        return self.__len_seq

    def len_min(self):
        return self.__len_min

    def min(self):
        return self.__min

    def max(self):
        return self.__max

    def len_max(self):
        return self.__len_max

    def mean(self):
        return self.__mean

    def harmonic_mean(self):
        return harmonic_mean(self.__sequence)

    def median(self):
        return self.__median

    def median_low(self):
        return median_low(self.__sequence)

    def median_high(self):
        return median_high(self.__sequence)

    def stdev(self):
        return self.__stdev

    def pstdev(self):
        return pstdev(self.__sequence)

    def to_dict(self):
        return { "len_seq": self.__len_seq,
                 "len_min": self.__len_min,
                 "min": self.__min,
                 "len_max": self.__len_max,
                 "max": self.__max,
                 "mean": self.__mean,
                 "median": self.__median,
                 "stdev": self.__stdev}

    def to_string(self, join="\n", decimals=2):
        f = "{0:." + str(decimals) + "f}"
        return join.join(
            [item[0] + ": " + (f.format(item[1]) if isinstance(item[1], float) else str(item[1])) for item in
             self.to_dict().items()])


class NlDialect(object):
    delimiter = ';'
    quotechar = '"'
    escapechar = None
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL