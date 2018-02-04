#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QPlainTextEdit

from core.services import Stat


class ClickableLabel(QLabel):

    clicked = pyqtSignal()

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class SelectableLabel(QLabel):

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)
        self.setContentsMargins(5, 1, 5, 1)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)


class StatView(QWidget):

    def __init__(self, parent=None, stat: Stat=None, title="statistics", decimals=2):
        QWidget.__init__(self, parent)
        vbl0 = QVBoxLayout(self)
        vbl0.setContentsMargins(0, 0, 0, 0)
        vbl0.setSpacing(0)
        self.__stat = stat
        self.decimals = decimals

        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet("font-weight: bold;")
        self.lbl_title.setText(title)
        vbl0.addWidget(self.lbl_title)

        self.stat_edit = QPlainTextEdit()
        self.stat_edit.setReadOnly(True)
        vbl0.addWidget(self.stat_edit)

        self.set_stat(self.__stat)

    def set_stat(self, stat: Stat):
        self.__stat = stat
        if stat is not None:
            self.stat_edit.clear()
            self.stat_edit.appendPlainText(stat.to_string(decimals=self.decimals))



