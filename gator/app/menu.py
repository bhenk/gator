#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction


class GMenuBar(QMenuBar):

    sgn_new_viewer = pyqtSignal(bool)

    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)
        self.addMenu(FileMenu(self))
        self.addMenu(ViewMenu(self))


class FileMenu(QMenu):

    def __init__(self, parent=None):
        QMenu.__init__(self, "File", parent)

        action_open_file = QAction("Open file", self)
        self.addAction(action_open_file)


class ViewMenu(QMenu):

    def __init__(self, parent=None):
        QMenu.__init__(self, "View", parent)

        action_new_viewer = QAction("New viewer", self)
        action_new_viewer.triggered.connect(GMenuBar.sgn_new_viewer)
        self.addAction(action_new_viewer)


