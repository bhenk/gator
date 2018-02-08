#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import subprocess

import exifread
from PyQt5.QtCore import Qt, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QKeyEvent, QCloseEvent, QMouseEvent, QFont
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QPushButton, \
    QHBoxLayout, QLayout, QMenu, QAction, QFrame, QMessageBox

from app.style import Style
from app.widgets import BrowserWindow
from bdbs.obj import Resource
from core.navigator import Navigator
from core.services import Format
from gwid.gwidget import StatView
from gwid.util import GIcon, GHotKey

MAX_SIZE = 16777215
MIN_SIZE = 0

LOG = logging.getLogger(__name__)


class Viewer(QLabel):

    sgn_resource_changed = pyqtSignal(Resource)

    def __init__(self, parent, navigator):
        QLabel.__init__(self)
        self.parent = parent
        self.navigator = navigator  # type: Navigator
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.ctrl = QApplication.instance().ctrl
        self.connect_signals()
        self.scale_screen_size = self.ctrl.config.viewer_scale_screen_size()

        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.browser_window = None

        self.move(self.ctrl.config.viewer_window_x(), self.ctrl.config.viewer_window_y())
        self.pixmap = None

        # actions
        self.menu_close_viewer = self.ctrl.menu_close_viewer()  # type: QMenu
        self.menu_edit = self.ctrl.menu_edit()  # type: QMenu
        self.menu_window = self.ctrl.menu_window()  # type: QMenu

        self.action_close_me = QAction("no name", self)
        self.action_close_me.triggered.connect(self.close)
        self.menu_close_viewer.addAction(self.action_close_me)

        self.action_acme_me = QAction("Acme me", self)
        self.action_acme_me.setShortcut("Ctrl+A")
        self.action_acme_me.triggered.connect(self.acme_me)

        self.action_copy_filename = QAction("Copy filename")
        self.action_copy_filename.triggered.connect(self.copy_filename)

        self.action_copy_pixmap = QAction("Copy image")
        self.action_copy_pixmap.triggered.connect(self.copy_pixmap)

        self.action_activate_me = QAction("no name", self)
        self.action_activate_me.triggered.connect(self.activate_self)
        self.action_activate_me.setCheckable(True)
        self.menu_window.addAction(self.action_activate_me)

        self.current_resource = None  # type: Resource
        self.set_resource(self.navigator.current_resource())
        self.view_control = ViewControl(self)
        self.popup = ViewerPopup(self)
        self.show()

    def connect_signals(self):
        self.ctrl.sgn_main_window_closing.connect(self.on_main_window_closing)
        self.ctrl.sgn_switch_resources.connect(self.on_sgn_switch_resources)

    def on_sgn_switch_resources(self):
        LOG.debug("sgn_switch_resources received")
        self.navigator = Navigator(self.ctrl.store, self.ctrl.resources)

    def resizeEvent(self, event):
        pixmap = self.pixmap.scaled(event.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(pixmap)
        self.resize(pixmap.size())

    def set_resource(self, resource: Resource):
        pixmap = QPixmap(resource.filename())
        if pixmap.isNull():
            self.ctrl.warn("Unable to load %s" % resource.filename())
            if self.pixmap is None:
                self.pixmap = QPixmap(150, 300)
        else:
            self.current_resource = resource
            self.pixmap = pixmap
            if self.scale_screen_size:
                rect = QApplication.desktop().screenGeometry()
                max_height = rect.height() - self.pos().y() - 50
                max_width = rect.width() - self.pos().x() - 5
                pixmap_scaled = self.pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.setPixmap(pixmap_scaled)
                self.resize(pixmap_scaled.size())
            else:
                self.setPixmap(self.pixmap)
                self.resize(self.pixmap.size())

            self.setWindowTitle(self.current_resource.long_name())
            self.action_close_me.setText(self.current_resource.long_name())
            self.action_activate_me.setText(self.current_resource.long_name())
            self.action_acme_me.setText("Acme %s" % self.current_resource.slv_index())
            self.ctrl.store.view_date_store().add_date_on(self.current_resource)
            self.ctrl.sgn_resource_changed.emit(self.current_resource)
        self.sgn_resource_changed.emit(self.current_resource)

    def keyPressEvent(self, event: QKeyEvent):
        self.ctrl.set_last_viewer(self)
        if GHotKey.matches(event):
            return
        elif event.nativeModifiers() == 1048840:
            if event.key() == Qt.Key_A:  # Ctrl+Acme
                self.acme_me()

    def acme_me(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("ACME")
        msg_box.setText("Acme %s" % self.current_resource.long_name())
        msg_box.setInformativeText("Ok to proceed?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setDefaultButton(QMessageBox.Yes)
        exe = msg_box.exec()
        if exe == QMessageBox.Yes:
            self.ctrl.store.acme_date_store().add_date_on(self.current_resource)
            self.sgn_resource_changed.emit(self.current_resource)

    def event(self, event: QEvent):
        if event.type() == QEvent.WindowActivate:
            self.action_activate_me.setChecked(True)
            self.menu_edit.insertAction(self.menu_edit.actions()[0], self.action_copy_pixmap)
            self.menu_edit.insertAction(self.menu_edit.actions()[0], self.action_copy_filename)
            self.menu_edit.insertAction(self.menu_edit.actions()[0], self.action_acme_me)
            self.ctrl.set_last_viewer(self)
            return True
        elif event.type() == QEvent.WindowDeactivate:
            self.action_activate_me.setChecked(False)
            self.menu_edit.removeAction(self.action_copy_pixmap)
            self.menu_edit.removeAction(self.action_copy_filename)
            self.menu_edit.removeAction(self.action_acme_me)
            return True
        return QWidget.event(self, event)

    def activate_main_window(self):
        main_window = QApplication.instance().main_window
        main_window.showNormal()
        main_window.raise_()
        main_window.activateWindow()
        gframe = main_window.gframe
        gframe.set_resource(self.current_resource)
        self.ctrl.set_last_viewer(self)

    def activate_self(self):
        self.view_control.activate_self()
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def toggle_control(self):
        if self.view_control.isActiveWindow():
            self.showNormal()
            self.raise_()
            self.activateWindow()
        else:
            self.view_control.showNormal()
            self.view_control.raise_()
            self.view_control.activateWindow()

    def go_file_down(self):
        self.set_resource(self.navigator.go_down())

    def go_file_up(self):
        self.set_resource(self.navigator.go_up())

    def go_file_left(self):
        self.set_resource(self.navigator.go_left())

    def go_file_right(self):
        self.set_resource(self.navigator.go_right())

    def go_file_start(self):
        self.set_resource(self.navigator.go_start())

    def toggle_scale_screen_size(self, checked):
        self.scale_screen_size = checked
        self.set_resource(self.current_resource)

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
        if self.current_resource.has_file():
            subprocess.call(['open', '-a', 'Preview', self.current_resource.filename()])

    def copy_filename(self):
        QApplication.clipboard().setText(self.current_resource.filename())

    def copy_pixmap(self):
        QApplication.clipboard().setPixmap(self.pixmap)

    def show_exif_data(self):
        if self.current_resource.has_file():
            self.browser_window = BrowserWindow()
            with open(self.current_resource.filename(), "rb") as file:
                exif = exifread.process_file(file)
                for k in sorted(exif.keys()):
                    self.browser_window.append("%s: \t %s" % (k, exif[k]))
            self.browser_window.show()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self.popup.popup(event.globalPos())

    def on_main_window_closing(self):
        LOG.debug("Received signal main window closing")
        self.close()

    def closeEvent(self, event: QCloseEvent):
        # Close events are sent to widgets that the user wants to close,
        # usually by choosing "Close" from the window menu,
        # or by clicking the X title bar button.
        # They are also sent when you call QWidget::close() to close a widget programmatically.
        LOG.debug("Close event on %s %s" % (self.__class__.__name__, self.windowTitle()))
        self.persist()
        if self.view_control is not None:
            self.view_control.close()
        self.menu_close_viewer.removeAction(self.action_close_me)
        self.menu_window.removeAction(self.action_activate_me)
        event.accept()

    def persist(self):
        self.ctrl.config.set_viewer_window_x(self.pos().x())
        self.ctrl.config.set_viewer_window_y(self.pos().y())
        self.ctrl.config.set_viewer_scale_screen_size(self.scale_screen_size)


class ViewControl(QWidget):

    def __init__(self, viewer: Viewer):
        QWidget.__init__(self, None)
        self.viewer = viewer
        self.ctrl = QApplication.instance().ctrl
        self.max_width = 165

        vbl_0 = QVBoxLayout(self)
        vbl_0.setContentsMargins(10, 5, 0, 5)  # left, top, right, bottom
        vbl_0.setSizeConstraint(QLayout.SetFixedSize)

        self.lbl_current_resource = QLabel()
        self.lbl_current_resource.setMaximumWidth(self.max_width)
        self.lbl_current_resource.setFont(QFont("Courier New", 12))
        self.lbl_current_resource.setStyleSheet(Style.bold())
        self.lbl_current_resource.setTextFormat(Qt.RichText)
        self.lbl_current_resource.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.lbl_current_resource.setOpenExternalLinks(True)
        vbl_0.addWidget(self.lbl_current_resource)

        self.lbl_current_image = QLabel()
        self.lbl_current_image.setMaximumWidth(self.max_width)
        vbl_0.addWidget(self.lbl_current_image, 1)

        self.lbl_acme_dates = QLabel()
        self.lbl_acme_dates.setWordWrap(True)
        self.lbl_acme_dates.setStyleSheet("background-color: yellow;")
        vbl_0.addWidget(self.lbl_acme_dates)

        self.lbl_view_dates = QLabel()
        self.lbl_view_dates.setWordWrap(True)
        vbl_0.addWidget(self.lbl_view_dates)

        # Navigator items
        navigator_line = QFrame()
        navigator_line.setFrameShape(QFrame.HLine)
        navigator_line.setFrameShadow(QFrame.Sunken)
        vbl_0.addWidget(navigator_line)

        self.stat_view_views = StatView(parent=self, title="View stats", decimals=4)
        self.stat_view_views.setMaximumSize(self.max_width, 155)
        vbl_0.addWidget(self.stat_view_views)

        # Navigate
        navigate_line = QFrame()
        navigate_line.setFrameShape(QFrame.HLine)
        navigate_line.setFrameShadow(QFrame.Sunken)
        vbl_0.addWidget(navigate_line)

        self.toggle_scale_screen_size = QCheckBox("scale screen size")
        self.toggle_scale_screen_size.setChecked(self.viewer.scale_screen_size)
        self.toggle_scale_screen_size.toggled.connect(self.viewer.toggle_scale_screen_size)
        vbl_0.addWidget(self.toggle_scale_screen_size)

        self.toggle_max_height = QCheckBox("fixed max height", self)
        self.toggle_max_height.toggled.connect(self.on_toggle_max_height)
        vbl_0.addWidget(self.toggle_max_height)

        self.toggle_max_width = QCheckBox("fixed max width", self)
        self.toggle_max_width.toggled.connect(self.on_toggle_max_width)
        vbl_0.addWidget(self.toggle_max_width)

        grid = QGridLayout()
        grid.setSpacing(0)

        button_up = QPushButton(self)
        button_up.setIcon(GIcon.arr_up())
        button_up.clicked.connect(self.viewer.go_file_up)
        grid.addWidget(button_up, 0, 1)

        button_left = QPushButton(self)
        button_left.setIcon(GIcon.arr_left())
        button_left.clicked.connect(self.viewer.go_file_left)
        grid.addWidget(button_left, 1, 0)

        button_right = QPushButton(self)
        button_right.setIcon(GIcon.arr_right())
        button_right.clicked.connect(self.viewer.go_file_right)
        grid.addWidget(button_right, 1, 2)

        button_down = QPushButton(self)
        button_down.setIcon(GIcon.arr_down())
        button_down.clicked.connect(self.viewer.go_file_down)
        grid.addWidget(button_down, 2, 1)

        self.btn_history_index = QPushButton(self)
        # self.btn_history_index.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(0, 0, 0);")
        # self.btn_history_index.setMaximumSize(40, 20)
        self.btn_history_index.clicked.connect(self.viewer.go_file_start)
        grid.addWidget(self.btn_history_index, 1, 1)

        hbox = QHBoxLayout()
        hbox.addLayout(grid)
        hbox.addStretch(1)
        vbl_0.addLayout(hbox)

        self.viewer.sgn_resource_changed.connect(self.on_resource_changed)
        self.on_resource_changed(self.viewer.current_resource)

        self.move(self.ctrl.config.viewer_control_window_x(), self.ctrl.config.viewer_control_window_y())
        self.show()

    def keyPressEvent(self, event: QKeyEvent):
        self.viewer.keyPressEvent(event)

    def activate_self(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    # https://stackoverflow.com/questions/3248243/gif-animation-in-qt
    # http://doc.qt.io/qt-5/qml-qtquick-animatedimage.html
    def on_resource_changed(self, resource: Resource):
        self.setWindowTitle(self.viewer.current_resource.basename())
        self.lbl_current_resource.setText(self.viewer.current_resource.hyperlink(slv_index=True))
        self.lbl_current_resource.setToolTip(self.viewer.current_resource.filename())

        pixmap = self.viewer.pixmap.scaled(self.max_width, MAX_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.lbl_current_image.setPixmap(pixmap)
        self.lbl_current_image.setToolTip(self.viewer.current_resource.filename())

        self.lbl_acme_dates.setVisible(self.viewer.current_resource.count_acme_dates() > 0)
        self.lbl_acme_dates.setText("\n".join(self.viewer.current_resource.acme_dates(fmt=Format.DATE_FULL)))

        self.lbl_view_dates.setText("\n".join(self.viewer.current_resource.view_dates(fmt=Format.DATE_FULL)))

        stat = self.viewer.navigator.stat_view_count()
        self.stat_view_views.set_stat(stat)

        self.btn_history_index.setText(str(self.viewer.current_resource.history_index()))
        self.btn_history_index.setEnabled(not self.viewer.navigator.is_at_start())
        self.toggle_max_height.setChecked(self.viewer.maximumHeight() != MAX_SIZE)
        self.toggle_max_width.setChecked(self.viewer.maximumWidth() != MAX_SIZE)

    def on_toggle_max_width(self, checked):
        self.viewer.toggle_max_width(checked)
        self.toggle_scale_screen_size.setEnabled(
            not (self.toggle_max_height.isChecked() or self.toggle_max_width.isChecked()))

    def on_toggle_max_height(self, checked):
        self.viewer.toggle_max_height(checked)
        self.toggle_scale_screen_size.setEnabled(
            not (self.toggle_max_height.isChecked() or self.toggle_max_width.isChecked()))

    def closeEvent(self, event: QCloseEvent):
        LOG.debug("Close event on Viewer Control")
        self.ctrl.config.set_viewer_control_window_x(self.pos().x())
        self.ctrl.config.set_viewer_control_window_y(self.pos().y())
        event.accept()


class ViewerPopup(QMenu):

    def __init__(self, viewer: Viewer):
        QMenu.__init__(self, "Viewer", viewer)
        self.viewer = viewer
        self.viewer.sgn_resource_changed.connect(self.on_resource_changed)

        action_control = QAction("Show/Hide Control", self)
        action_control.triggered.connect(viewer.toggle_control)
        self.addAction(action_control)

        self.action_preview = QAction("Open in Preview", self)
        self.action_preview.triggered.connect(viewer.open_in_preview)
        self.addAction(self.action_preview)

        self.addAction(viewer.action_copy_filename)
        self.addAction(viewer.action_copy_pixmap)

        self.action_exif_data = QAction("Show exif data", self)
        self.action_exif_data.triggered.connect(viewer.show_exif_data)
        self.addAction(self.action_exif_data)

        self.addSeparator()

        action_close = QAction("Close", self)
        action_close.triggered.connect(viewer.close)
        self.addAction(action_close)

    def on_resource_changed(self, resource: Resource):
        file_enabled = self.viewer.current_resource is not None
        self.action_preview.setEnabled(file_enabled)
        self.action_exif_data.setEnabled(file_enabled)

