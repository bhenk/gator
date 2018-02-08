#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu


class GMenuBar(QMenuBar):

    def __init__(self, parent=None):
        QMenuBar.__init__(self, parent)

        self.menu_file = self.addMenu("File")
        #self.menu_file.aboutToShow.connect(self.on_menu_file_about_to_show)
        self.menu_edit = self.addMenu("Edit")
        self.menu_view = self.addMenu("View")
        self.menu_window = self.addMenu("Window") # type: QMenu

        self.menu_close_viewer = self.menu_file.addMenu("Close viewer")
        self.action_close_viewers = QAction("Close all viewers", self)
        self.action_close_viewers.triggered.connect(self.on_close_all_viewers)
        self.menu_file.addAction(self.action_close_viewers)

        self.menu_file.addSection("main")

    # https://bugreports.qt.io/browse/QTBUG-56276
    def on_menu_file_about_to_show(self):
        print("=======================")
        for action in self.menu_file.actions():
            print(action.text())

    def on_close_all_viewers(self):
        for action in self.menu_close_viewer.actions():
            action.activate(QAction.Trigger)





