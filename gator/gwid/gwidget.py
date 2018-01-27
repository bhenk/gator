#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):

    clicked = pyqtSignal()

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()
