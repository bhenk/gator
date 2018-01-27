#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
from inspect import getframeinfo, currentframe

from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout, QHBoxLayout
from app.style import Style
from app.viewer import Viewer
from core.configuration import PathFinder, GatorConf
from core.navigator import Resources, Navigator
from gwid.listdialog import GPathListDialog
from gwid.util import GIcon

LOG = logging.getLogger(__name__)


class GFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.sgn_switch_configuration.connect(self.on_sgn_switch_configuration)
        self.ctrl.sgn_switch_resources.connect(self.on_sgn_switch_resources)
        self.path_finder = self.ctrl.path_finder  # type: PathFinder
        self.config = self.ctrl.config  # type: GatorConf
        self.resources = self.ctrl.resources  # type: Resources

        vbl0 = QVBoxLayout(self)
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        # grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)
        # grid.setHorizontalSpacing(5)
        vbl0.addLayout(grid)
        lbl_config = QLabel("configuration")
        self.path_combo = QComboBox(self)
        self.path_combo.currentIndexChanged.connect(self.on_path_combo_changed)
        btn_path = QPushButton("...")
        btn_path.clicked.connect(self.on_btn_path_clicked)
        grid.addWidget(lbl_config, 0, 0)
        grid.addWidget(self.path_combo, 0, 1)
        grid.addWidget(btn_path, 0, 2)

        self.lbl_resources_count = QLabel(self.resources.to_string())
        self.lbl_resources_count.setStyleSheet(Style.blue_text() + Style.bold())
        btn_resources = QPushButton("...")
        btn_resources.clicked.connect(self.on_btn_resources_clicked)
        grid.addWidget(self.lbl_resources_count, 1, 0, 2, 0)
        grid.addWidget(btn_resources, 1, 2)

        vbl0.addStretch(1)

        btn_box = QHBoxLayout()
        vbl0.addLayout(btn_box)
        btn_box.addStretch(1)

        self.btn_viewer = QPushButton()
        self.btn_viewer.setIcon(GIcon.viewer())
        self.btn_viewer.clicked.connect(self.on_btn_viewer_clicked)
        btn_box.addWidget(self.btn_viewer)

        self.set_path_finder_items()

    # ##### configuration file #####
    def set_path_finder_items(self):
        self.path_combo.clear()
        self.path_combo.addItems(self.path_finder.path_list())

    def on_btn_path_clicked(self):
        pd = GPathListDialog(self, self.path_finder.path_list(), window_title="Configuration file",
                             mode=GPathListDialog.MODE_SAVE_FILE_NAME,
                             start_path=os.path.expanduser("~/gator.cfg"))
        pd.deleteLater()
        if pd.exec():
            self.path_finder.set_path_list(pd.str_list())
            self.path_finder.persist()
            self.set_path_finder_items()

    # result of user interaction or programmatic change
    def on_path_combo_changed(self, index):
        if index > -1:
            if self.path_finder.dir_exists(index):
                self.ctrl.switch_configuration(self.path_finder.path_list()[index])
            else:
                self.ctrl.warn("%s does not exist" % self.path_finder.path_list()[index])
                self.path_combo.setCurrentIndex(self.ctrl.configuration_index)

    def on_sgn_switch_configuration(self):
        LOG.debug("sgn_switch_configuration received")
        self.config = self.ctrl.config  # type: GatorConf
        self.resources = self.ctrl.resources  # type: Resources
        self.path_combo.setCurrentIndex(self.ctrl.configuration_index)
        self.lbl_resources_count.setText(self.resources.to_string())

    # ##### resources #####
    def on_sgn_switch_resources(self):
        LOG.debug("sgn_switch_resources received")
        self.resources = self.ctrl.resources  # type: Resources
        self.lbl_resources_count.setText(self.resources.to_string())
        self.btn_viewer.setEnabled(self.resources.resource_count() > 0)

    def on_btn_resources_clicked(self):
        pd = GPathListDialog(self, self.resources.path_list(), window_title="Resources",
                             mode=GPathListDialog.MODE_EXISTING_DIRECTORY,
                             start_path=os.path.dirname(self.ctrl.gator_home), allow_duplicates=True)
        pd.deleteLater()
        if pd.exec():
            self.config.set_resources(pd.str_list())
            self.config.persist()
            self.ctrl.switch_resources()

    # ##### viewers #####
    def on_btn_viewer_clicked(self):
        navigator = Navigator(self.resources)
        Viewer(self, navigator)


    def mousePressEvent(self, QMouseEvent):
        print("mouse pressed")


