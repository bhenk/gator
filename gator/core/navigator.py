#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random


EXTENSIONS = ['.jpg', '.bmp', '.png', '.gif']


class Navigator(object):

    def __init__(self, resource_dir):
        self.resource_dir = resource_dir
        self.file_list = self.list_files(self.resource_dir)
        self.history_list = []
        self.pointer = 0
        self.current_file = self.random_file()
        self.history_list.append(self.current_file)

    @staticmethod
    def list_files(base_directory):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(base_directory):
            for fi in filenames:
                if os.path.splitext(fi)[1].lower() in EXTENSIONS:
                    f.append(dirpath + "/" + fi)
        return f

    def random_file(self):
        if len(self.file_list) > 0:
            nmbr = random.randint(0, len(self.file_list) - 1)
            return self.file_list[nmbr]
        else:
            return None

    def go_down(self):
        self.pointer += 1
        if self.pointer > len(self.history_list) - 1:
            self.current_file = self.random_file()
            self.history_list.append(self.current_file)
        else:
            self.current_file = self.history_list[self.pointer]
        return self.current_file

    def go_up(self):
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = 0
        self.current_file = self.history_list[self.pointer]
        return self.current_file

    def go_left(self):
        return self.go_lateral(-1)

    def go_right(self):
        return self.go_lateral(1)

    def go_lateral(self, inc=1):
        if self.current_file is None:
            return None
        current_dir = os.path.dirname(self.current_file)
        f = []
        for (dirpath, dirnames, filenames) in os.walk(current_dir):
            for fi in filenames:
                if os.path.splitext(fi)[1].lower() in EXTENSIONS:
                    f.append(dirpath + "/" + fi)
        point = f.index(self.current_file)
        point += inc
        if (point < 0):
            point = 0
        if point > len(f) - 1:
            point = len(f) - 1
        new_file = f[point]
        if new_file != self.current_file:
            self.current_file = new_file
            self.history_list.append(self.current_file)
            self.pointer = len(self.history_list) - 1
        return self.current_file


