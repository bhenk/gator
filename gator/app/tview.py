#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QPushButton
from app.viewer import Viewer

LOG = logging.getLogger(__name__)


class ViewFrame(QFrame):

    def __init__(self, parent, index=-1):
        super().__init__(parent)
        self.index = index
        self.ctrl = QApplication.instance().ctrl
        self.init_ui()
        self.viewers = []

    def init_ui(self):
        vbl_0 = QVBoxLayout(self)

        viewer_button = QPushButton("New viewer")
        viewer_button.clicked.connect(self.viewer_button_clicked)
        vbl_0.addWidget(viewer_button)

        self.setLayout(vbl_0)

    def viewer_button_clicked(self):
        viewer = Viewer(self)
        self.viewers.append(viewer)
