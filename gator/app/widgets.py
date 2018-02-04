#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QDesktopServices
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QTextBrowser, \
    QVBoxLayout, QHBoxLayout, QGridLayout

import version
from app.style import Style

LOG = logging.getLogger(__name__)


# ################################################################
class SelectableLabel(QLabel):

    def __init__(self, *__args):
        QLabel.__init__(self, *__args)
        self.setContentsMargins(5, 1, 5, 1)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setStyleSheet(Style.derived())


class BrowserWindow(QTextBrowser):

    def __init__(self):
        QTextBrowser.__init__(self)
        # self.setWindowTitle("Exif data")
        # vbox = QVBoxLayout(self)
        # self.browser = QTextBrowser(self)
        # vbox.addWidget(self.browser)
        # self.setLayout(vbox)


class AboutWidget(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self)
        self.ctrl = QApplication.instance().ctrl
        self.parent = parent
        self.setWindowTitle("About")
        hbox = QHBoxLayout()
        # pic = QLabel(self)
        # pix = QPixmap(os.path.join(self.ctrl.application_home, 'conf/img/logo_h.png'))
        # pic.setPixmap(pix)
        # hbox.addWidget(pic)

        vbox = QVBoxLayout()

        lbl_title = QLabel("Gator", self)
        lbl_title.setMinimumWidth(400)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        lbl_title.setFont(font)
        lbl_title.setContentsMargins(2, 5, 5, 7)
        lbl_title.setStyleSheet(Style.h2())
        vbox.addWidget(lbl_title)
        #vbox.addSpacing(20)
        vbox.addStretch(1)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(2)
        grid.setHorizontalSpacing(2)

        grid.addWidget(QLabel("Version: "), 1, 1)
        grid.addWidget(QLabel(version.__version__), 1, 2)

        grid.addWidget(QLabel("Release: "), 2, 1)
        grid.addWidget(QLabel(version.__release_date__), 2, 2)

        hbox_grid = QHBoxLayout()
        hbox_grid.addLayout(grid)
        hbox_grid.addStretch(1)
        vbox.addLayout(hbox_grid)

        vbox.addSpacing(10)
        txt = QTextBrowser()
        txt.setMinimumHeight(250)
        txt.setOpenExternalLinks(True)
        txt.setOpenLinks(False)
        txt.anchorClicked.connect(self.on_anchor_clicked)
        txt.append(version.__about__)
        vbox.addWidget(txt)

        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)
        self.move(200, 200)
        self.setWindowFlags( (self.windowFlags() | Qt.CustomizeWindowHint) & ~Qt.WindowMaximizeButtonHint & ~Qt.WindowMinimizeButtonHint)
        self.show()

    def on_anchor_clicked(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # def close(self):
    #     self.parent.about_widget = None
    #     super(AboutWidget, self).close()
    #
    # def closeEvent(self, event):
    #     self.close()
    #     event.accept()
