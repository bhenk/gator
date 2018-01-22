#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout
from core.configuration import PathFinder
from gwid.listdialog import GPathListDialog

LOG = logging.getLogger(__name__)


class GFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.path_finder = self.ctrl.path_finder
        self.ctrl.sgn_switch_configuration.connect(self.on_switch_configuration)

        vbl0 = QVBoxLayout(self)
        grid = QGridLayout()
        grid.setColumnStretch(2, 1)
        # grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)
        # grid.setHorizontalSpacing(5)
        vbl0.addLayout(grid)
        lbl_config = QLabel("configuration")
        self.path_combo = QComboBox(self)
        self.path_combo.currentIndexChanged.connect(self.on_path_combo_changed)
        btn_path = QPushButton("...")
        btn_path.clicked.connect(self.on_btn_path_clicked)
        grid.addWidget(lbl_config, 1, 1)
        grid.addWidget(self.path_combo, 1, 2)
        grid.addWidget(btn_path, 1, 3)

        lbl_resources = QLabel("resources")
        self.lbl_resources_count = QLabel("0")
        btn_resources = QPushButton("...")
        btn_resources.clicked.connect(self.on_btn_resources_clicked)
        grid.addWidget(lbl_resources, 2, 1)
        grid.addWidget(self.lbl_resources_count, 2, 2)
        grid.addWidget(btn_resources, 2, 3)

        vbl0.addStretch(1)
        self.on_path_finder_change()

    # configuration path #####
    def on_path_finder_change(self):
        self.path_combo.clear()
        self.path_combo.addItems(self.path_finder.path_list())

    def on_btn_path_clicked(self):
        pd = GPathListDialog(self, self.path_finder.path_list(), mode=GPathListDialog.MODE_SAVE_FILE_NAME,
                             start_path=os.path.expanduser("~/gator.cfg"))
        pd.deleteLater()
        if pd.exec():
            self.path_finder.set_path_list(pd.str_list())
            self.path_finder.persist()
            self.on_path_finder_change()

    def on_path_combo_changed(self, index):
        if index >= 0:
            configuration_file = self.path_finder.path_list()[index]
            if self.ctrl.configuration_file != configuration_file:
                self.ctrl.switch_configuration(configuration_file)

    def on_switch_configuration(self):
        if self.path_combo.currentIndex() != self.ctrl.configuration_index:
            self.path_combo.setCurrentIndex(self.ctrl.configuration_index)

    # resources #####
    def on_btn_resources_clicked(self):
        pd = GPathListDialog(self, self.ctrl.config.resources(), mode=GPathListDialog.MODE_EXISTING_DIRECTORY,
                             start_path=os.path.dirname(self.ctrl.gator_home))
        pd.deleteLater()
        if pd.exec():
            self.ctrl.config.set_resources(pd.str_list())


    def mousePressEvent(self, QMouseEvent):
        print("mouse pressed")


