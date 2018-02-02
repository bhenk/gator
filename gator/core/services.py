#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from statistics import mean, harmonic_mean, median, median_low, median_high, stdev, pstdev


def application_home():
    if getattr(sys, 'frozen', False):
        # running in a bundle
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


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
        self.__sequence = [0] if len(sequence) == 0 else sequence

    def len(self):
        return len(self.__sequence)

    def len_min(self):
        m = self.min()
        return len([x for x in self.__sequence if x == m])

    def min(self):
        return min(self.__sequence)

    def max(self):
        return max(self.__sequence)

    def mean(self):
        return mean(self.__sequence)

    def harmonic_mean(self):
        return harmonic_mean(self.__sequence)

    def median(self):
        return median(self.__sequence)

    def median_low(self):
        return median_low(self.__sequence)

    def median_high(self):
        return median_high(self.__sequence)

    def stdev(self):
        return -1 if len(self.__sequence) < 2 else stdev(self.__sequence)

    def pstdev(self):
        return pstdev(self.__sequence)

    def to_dict(self):
        return { "len": self.len(),
                 "len_min": self.len_min(),
                 "min": self.min(),
                 "max": self.max(),
                 "mean": self.mean(),
                 "median": self.median(),
                 "stdev": self.stdev(),
                 "pstdev": self.pstdev()}

    def to_string(self, join="\n", decimals=2):
        f = "{0:." + str(decimals) + "f}"
        return join.join(
            [item[0] + ": " + (f.format(item[1]) if isinstance(item[1], float) else str(item[1])) for item in
             self.to_dict().items()])
