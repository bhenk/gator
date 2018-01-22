#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton
from app.widgets import AboutWidget

LOG = logging.getLogger(__name__)


class ConfigureFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.init_ui()

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)

        # self.para_widgets = {
        #     "resource_dir": ParaLineEdit(self, "resource_dir", ParaWidget.str_conv(), grid, 3, True)
        # }

        vbl_0.addLayout(grid)
        vbl_0.addStretch(1)

        button_about = QPushButton("About")
        button_about.clicked.connect(self.show_about)
        vbl_0.addWidget(button_about)
        self.about_widget = None
        self.setLayout(vbl_0)

    def show_about(self):
        self.about_widget = AboutWidget(self)

    def count_errors(self):
        return len([p for p in self.para_widgets.values() if not p.is_accepted()])