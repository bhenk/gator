#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QKeySequence
from PyQt5.QtWidgets import QFrame, QApplication, QVBoxLayout, QLabel, QComboBox, QPushButton, QGridLayout, QWidget, \
    QFileDialog, QAction, QMenu

from app.style import Style
from app.viewer import Viewer
from bdbs.obj import Resource
from core.configuration import PathFinder, GatorConf
from core.navigator import Resources, Navigator
from core.services import Format
from gwid.gwidget import ClickableLabel
from gwid.listdialog import GPathListDialog
from gwid.util import GIcon

LOG = logging.getLogger(__name__)

MAX_SIZE = 16777215


class GFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.ctrl_v = QKeySequence.fromString("Ctrl+V", 0)

        self.ctrl = QApplication.instance().ctrl
        self.ctrl.sgn_switch_configuration.connect(self.on_sgn_switch_configuration)
        self.ctrl.sgn_switch_resources.connect(self.on_sgn_switch_resources)
        self.ctrl.sgn_main_window_closing.connect(self.on_main_window_closing)

        self.path_finder = self.ctrl.path_finder  # type: PathFinder
        self.config = self.ctrl.config  # type: GatorConf
        self.resources = self.ctrl.resources  # type: Resources

        vbl0 = QVBoxLayout(self)
        vbl0.setSpacing(5)
        # vbl0.setContentsMargins(3, 3, 3, 0)
        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        grid.setContentsMargins(0, 0, 0, 0)  # left, top, right, bottom
        grid.setVerticalSpacing(5)
        vbl0.addLayout(grid)
        lbl_config = QLabel("configuration")
        self.path_combo = QComboBox(self)
        self.path_combo.currentIndexChanged.connect(self.on_path_combo_changed)
        btn_path = QPushButton("...")
        btn_path.clicked.connect(self.show_configuration_window)
        grid.addWidget(lbl_config, 0, 0)
        grid.addWidget(self.path_combo, 0, 1)
        grid.addWidget(btn_path, 0, 2)

        self.btn_viewer = QPushButton(self.ctrl_v.toString(0))
        self.btn_viewer.setStyleSheet(Style.green_text())
        self.btn_viewer.setShortcut(self.ctrl_v)
        self.btn_viewer.setIcon(GIcon.viewer())
        self.btn_viewer.clicked.connect(self.on_btn_viewer_clicked)
        self.lbl_resources_count = QLabel(self.resources.to_string())
        self.lbl_resources_count.setStyleSheet(Style.green_text() + Style.bold())

        btn_resources = QPushButton("...")
        btn_resources.clicked.connect(self.show_resources_window)
        grid.addWidget(self.btn_viewer, 1, 0)
        grid.addWidget(self.lbl_resources_count, 1, 1)
        grid.addWidget(btn_resources, 1, 2)

        # actions
        self.menu_file = self.ctrl.menu_file()  # type: QMenu
        self.menu_view = self.ctrl.menu_view()  # type: QMenu
        self.menu_edit = self.ctrl.menu_edit()  # type: QMenu

        action_open_file = QAction("Open file...", self)
        action_open_file.setShortcut("Ctrl+O")
        action_open_file.setIcon(GIcon.open_file())
        action_open_file.triggered.connect(self.on_open_file)
        self.menu_file.insertAction(self.menu_file.actions()[0], action_open_file)

        action_new_viewer = QAction("New &viewer", self)
        action_new_viewer.setIcon(GIcon.viewer_white())
        action_new_viewer.setShortcut("Ctrl+V")
        action_new_viewer.triggered.connect(self.on_btn_viewer_clicked)
        self.menu_view.addAction(action_new_viewer)

        self.menu_edit.addSeparator()
        action_show_configuration = QAction("Gator cfg...", self)
        action_show_configuration.setIcon(GIcon.configuration())
        action_show_configuration.triggered.connect(self.show_configuration_window)
        self.menu_edit.addAction(action_show_configuration)

        action_show_resources = QAction("Resources...", self)
        action_show_resources.setIcon(GIcon.resources())
        action_show_resources.triggered.connect(self.show_resources_window)
        self.menu_edit.addAction(action_show_resources)

        self.next_navigator = Navigator(self.ctrl.store, self.resources)
        first_resource = self.next_navigator.current_resource()
        self.image_frame = ResourceWidget(self, first_resource, 200)
        vbl0.addWidget(self.image_frame, 1)

        self.set_path_finder_items()

    # ##### configuration file #####
    def set_path_finder_items(self):
        self.path_combo.clear()
        self.path_combo.addItems(self.path_finder.path_list())

    def show_configuration_window(self):
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

    def show_resources_window(self):
        pd = GPathListDialog(self, self.resources.path_list(), window_title="Resources",
                             mode=GPathListDialog.MODE_EXISTING_DIRECTORY,
                             start_path=os.path.dirname(self.ctrl.gator_home), allow_duplicates=True)
        pd.deleteLater()
        if pd.exec():
            self.config.set_resources(pd.str_list())
            self.config.persist()
            self.ctrl.switch_resources()

    # ##### viewers #####
    def on_btn_viewer_clicked(self, *args):
        # first viewer is created with navigator used for ResourceWidget
        if self.next_navigator is None:
            self.next_navigator = Navigator(self.ctrl.store, self.resources)
        Viewer(self, self.next_navigator)
        self.next_navigator = None

    def set_resource(self, resource: Resource):
        self.image_frame.set_resource(resource)

    def on_main_window_closing(self):
        LOG.debug("Received signal main window closing")

    def on_open_file(self, *args):
        common_prefix = self.resources.common_prefix()
        LOG.debug("Get open filename from %s" % common_prefix)
        filename = QFileDialog.getOpenFileName(self, "Open File", common_prefix, filter=Resources.filter_list())
        if filename[0] != "":
            if filename[0] in self.resources.resource_list():
                Viewer(self, Navigator(self.ctrl.store, self.resources, filename[0]))
            else:
                self.ctrl.info("%s not in resource list" % filename[0])


# ##### ##########################################################
class ResourceWidget(QWidget):

    def __init__(self, parent, resource: Resource, initial_img_size=200):
        super().__init__(parent)
        self.ctrl = QApplication.instance().ctrl
        self.ctrl.sgn_resource_changed.connect(self.on_resource_changed)

        self.resource = resource
        self.pixmap = None
        self.setContentsMargins(0, 0, 0, 0)

        vbl0 = QVBoxLayout(self)
        vbl0.setContentsMargins(0, 0, 0, 0)
        vbl0.setSpacing(5)
        self.lbl_filename = QLabel()
        self.lbl_filename.setWordWrap(True)
        self.lbl_filename.setTextFormat(Qt.RichText)
        self.lbl_filename.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.lbl_filename.setOpenExternalLinks(True)
        self.lbl_image = ClickableLabel()
        self.lbl_image.clicked.connect(self.on_lbl_image_clicked)
        self.lbl_image.setMinimumSize(QSize(25, 25))
        # initial max size
        self.lbl_image.setFixedSize(QSize(initial_img_size, initial_img_size))
        self.lbl_viewed = QLabel()
        self.lbl_viewed.setWordWrap(True)

        vbl0.addWidget(self.lbl_filename)
        vbl0.addWidget(self.lbl_image, 1)
        vbl0.addWidget(self.lbl_viewed)

        self.set_resource(self.resource)

    def set_resource(self, resource: Resource):
        self.resource = resource
        if self.resource is not None:
            self.lbl_filename.setText(self.resource.hyperlink(split=True))
            self.pixmap = QPixmap(self.resource.filename())
            pixmap = self.pixmap.scaled(self.lbl_image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_image.setPixmap(pixmap)
            self.lbl_viewed.setText(" | ".join(self.resource.view_dates(fmt=Format.DATE_FULL)))
            self.updateGeometry()

    def resizeEvent(self, event):
        self.lbl_image.setMaximumSize(QSize(MAX_SIZE, MAX_SIZE))
        self.lbl_image.setMinimumSize(QSize(25, 25))
        if self.pixmap is not None:
            height = event.size().height() - self.lbl_filename.height() # -15 with menu bar
            size = QSize(event.size().width(), height)
            pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.lbl_image.setPixmap(pixmap)

    def on_lbl_image_clicked(self):
        self.parent().on_btn_viewer_clicked()

    def img_heigth(self):
        return self.lbl_image.height()

    def img_width(self):
        return self.lbl_image.width()

    def on_resource_changed(self, resource: Resource):
        if self.resource.filename() == resource.filename():
            self.resource = resource
            self.lbl_viewed.setText(" | ".join(self.resource.view_dates(fmt=Format.DATE_FULL)))
