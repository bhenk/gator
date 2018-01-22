#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from core.configuration import PathFinder
from gwid.listdialog import GPathListDialog

LOG = logging.getLogger(__name__)


class GFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.path_finder = PathFinder()
        self.ctrl.sgn_switch_configuration.connect(self.on_switch_configuration)

        vbl0 = QVBoxLayout(self)

        path_box = QHBoxLayout()
        path_box.addWidget(QLabel("configuration"))
        self.path_combo = QComboBox(self)
        self.path_combo.currentIndexChanged.connect(self.on_path_combo_changed)
        path_box.addWidget(self.path_combo, 1)
        self.on_path_finder_change()
        btn_path = QPushButton("...")
        btn_path.clicked.connect(self.on_btn_path_clicked)
        path_box.addWidget(btn_path)
        vbl0.addLayout(path_box)

        vbl0.addStretch(1)

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
        self.path_combo.setCurrentIndex(self.ctrl.configuration_index)

    def mousePressEvent(self, QMouseEvent):
        print("mouse pressed")


