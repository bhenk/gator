#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import subprocess

import exifread
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QKeyEvent, QCloseEvent, QMouseEvent
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QPushButton, \
    QHBoxLayout, QLayout, QMenu, QAction
from app.widgets import BrowserWindow
from core.navigator import Navigator

MAX_SIZE = 16777215
MIN_SIZE = 0

LOG = logging.getLogger(__name__)


class Viewer(QLabel):

    viewer_changed = pyqtSignal()

    def __init__(self, parent):
        QLabel.__init__(self)
        self.parent = parent
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.sgn_main_window_closing.connect(self.close)
        # self.ctrl.switch_configuration.connect(self.on_switch_configuration)

        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.popup = ViewerPopup(self)
        self.browser_window = None

        self.navigator = Navigator(self.ctrl.config.resource_dir())
        self.pixmap = None
        self.current_file = None
        self.filename = None
        self.dir_name = None
        self.set_file(self.navigator.current_file)

        self.view_control = None
        self.show()

    def on_switch_configuration(self):
        LOG.debug("Switch configuration")
        pass

    def resizeEvent(self, event):
        pixmap = self.pixmap.scaled(event.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.resize(pixmap.size())

    def set_file(self, file_name):
        pixmap = QPixmap(file_name)
        if pixmap.isNull():
            LOG.warning("Unable to load %s" % file_name)
            self.ctrl.warn("Unable to load %s" % file_name)
            if self.pixmap is None:
                self.pixmap = QPixmap(150, 300)
        else:
            self.current_file = file_name
            self.pixmap = pixmap
            self.setPixmap(self.pixmap)
            self.resize(self.pixmap.size())

            rel_file = os.path.relpath(self.current_file, self.ctrl.config.resource_dir())
            self.dir_name = os.path.dirname(rel_file)
            self.filename = os.path.basename(rel_file)
            self.setWindowTitle(self.filename)

        self.viewer_changed.emit()

    def keyPressEvent(self, event: QKeyEvent):
        # navigate
        if event.key() == Qt.Key_Down:
            self.go_file_down()
        elif event.key() == Qt.Key_Up:
            self.go_file_up()
        elif event.key() == Qt.Key_Left:
            self.go_file_left()
        elif event.key() == Qt.Key_Right:
            self.go_file_right()
        # toggle max size
        elif event.key() == Qt.Key_F1:
            self.toggle_max_height(self.maximumHeight() == MAX_SIZE)
            self.viewer_changed.emit()
        elif event.key() == Qt.Key_F2:
            self.toggle_max_width(self.maximumWidth() == MAX_SIZE)
            self.viewer_changed.emit()
        elif event.key() == 16777250: # Ctrl
            self.show_hide_control()

    def show_hide_control(self):
        if self.view_control is None:
            self.view_control = ViewControl(self)
        elif self.view_control.isHidden():
            self.view_control.show()
        elif self.view_control.isMinimized():
            self.view_control.showNormal()
        else:
            self.view_control.hide()

    def go_file_down(self):
        self.set_file(self.navigator.go_down())

    def go_file_up(self):
        self.set_file(self.navigator.go_up())

    def go_file_left(self):
        self.set_file(self.navigator.go_left())

    def go_file_right(self):
        self.set_file(self.navigator.go_right())

    def toggle_max_height(self, checked):
        if checked:
            self.setMaximumHeight(self.height())
        else:
            self.setMaximumHeight(MAX_SIZE)

    def toggle_max_width(self, checked):
        if checked:
            self.setMaximumWidth(self.width())
        else:
            self.setMaximumWidth(MAX_SIZE)

    def open_in_preview(self):
        if self.current_file:
            subprocess.call(['open', '-a', 'Preview', self.current_file])

    def copy_filename(self):
        QApplication.clipboard().setText(self.current_file)

    def show_exif_data(self):
        if self.current_file:
            self.browser_window = BrowserWindow()
            with open(self.current_file, "rb") as file:
                exif = exifread.process_file(file)
                for k in sorted(exif.keys()):
                    self.browser_window.append("%s: \t %s" % (k, exif[k]))
            self.browser_window.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.popup.popup(event.globalPos())

    def closeEvent(self, event: QCloseEvent):
        if self.view_control is not None:
            self.view_control.close()
        event.accept()


class ViewControl(QWidget):

    def __init__(self, viewer: Viewer):
        QWidget.__init__(self, None)
        self.viewer = viewer
        self.ctrl = viewer.ctrl

        vbl_0 = QVBoxLayout(self)
        vbl_0.setSizeConstraint(QLayout.SetFixedSize)

        self.btn_current_file = QPushButton("File", self)
        self.btn_current_file.setFlat(True)
        self.btn_current_file.setStyleSheet("Text-align:left")
        self.btn_current_file.clicked.connect(self.viewer.copy_filename)
        vbl_0.addWidget(self.btn_current_file)

        self.toggle_max_height = QCheckBox("fixed max height (F1)", self)
        self.toggle_max_height.toggled.connect(self.viewer.toggle_max_height)
        vbl_0.addWidget(self.toggle_max_height)

        self.toggle_max_width = QCheckBox("fixed max width (F2)", self)
        self.toggle_max_width.toggled.connect(self.viewer.toggle_max_width)
        vbl_0.addWidget(self.toggle_max_width)

        grid = QGridLayout()
        grid.setSpacing(0)

        button_up = QPushButton(self)
        button_up.setIcon(self.ctrl.icon("chevron-sign-up.png"))
        button_up.clicked.connect(self.viewer.go_file_up)
        grid.addWidget(button_up, 1, 2)

        button_left = QPushButton(self)
        button_left.setIcon(self.ctrl.icon("chevron-sign-left.png"))
        button_left.clicked.connect(self.viewer.go_file_left)
        grid.addWidget(button_left, 2, 1)

        button_right = QPushButton(self)
        button_right.setIcon(self.ctrl.icon("chevron-sign-right.png"))
        button_right.clicked.connect(self.viewer.go_file_right)
        grid.addWidget(button_right, 2, 3)

        button_down = QPushButton(self)
        button_down.setIcon(self.ctrl.icon("chevron-sign-down.png"))
        button_down.clicked.connect(self.viewer.go_file_down)
        grid.addWidget(button_down, 3, 2)

        hbox = QHBoxLayout()
        hbox.addLayout(grid)
        hbox.addStretch(1)
        vbl_0.addLayout(hbox)

        self.viewer.viewer_changed.connect(self.on_viewer_changed)
        self.on_viewer_changed()

        self.show()

    def keyPressEvent(self, event: QKeyEvent):
        self.viewer.keyPressEvent(event)

    def on_viewer_changed(self):
        if self.viewer.current_file is not None:
            self.btn_current_file.setText(self.viewer.dir_name + "\n" + self.viewer.filename)
        else:
            self.btn_current_file.setText("")

        self.toggle_max_height.setChecked(self.viewer.maximumHeight() != MAX_SIZE)
        self.toggle_max_width.setChecked(self.viewer.maximumWidth() != MAX_SIZE)


class ViewerPopup(QMenu):

    def __init__(self, viewer: Viewer):
        QMenu.__init__(self, "Viewer", viewer)
        self.viewer = viewer
        self.viewer.viewer_changed.connect(self.on_viewer_changed)

        action_control = QAction("Show/Hide Control", self)
        action_control.triggered.connect(viewer.show_hide_control)
        self.addAction(action_control)

        self.action_preview = QAction("Open in Preview", self)
        self.action_preview.triggered.connect(viewer.open_in_preview)
        self.addAction(self.action_preview)

        self.action_copy_filename = QAction("Copy filename", self)
        self.action_copy_filename.triggered.connect(viewer.copy_filename)
        self.addAction(self.action_copy_filename)

        self.action_exif_data = QAction("Show exif data", self)
        self.action_exif_data.triggered.connect(viewer.show_exif_data)
        self.addAction(self.action_exif_data)

        self.addSeparator()

        action_close = QAction("Close", self)
        #action_close.setShortcut("Ctrl+X")
        action_close.triggered.connect(viewer.close)
        self.addAction(action_close)

    def on_viewer_changed(self):
        file_enabled = self.viewer.current_file is not None
        self.action_preview.setEnabled(file_enabled)
        self.action_copy_filename.setEnabled(file_enabled)
        self.action_exif_data.setEnabled(file_enabled)

