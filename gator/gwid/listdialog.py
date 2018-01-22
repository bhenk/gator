#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QListView, QAbstractItemView, QPushButton, QFileDialog, \
    QInputDialog
from gwid import util


class GListDialog(QDialog):

    def __init__(self, parent, item_list=list(), window_title="Items"):
        QDialog.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.__str_list = list(item_list)
        self.setWindowTitle(window_title)

        vbox = QVBoxLayout(self)

        list_box = QHBoxLayout()
        vbox.addLayout(list_box)
        self.list_view = QListView()
        self.list_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_view.setAlternatingRowColors(True)
        self.standard_item_model = QStandardItemModel(self.list_view)
        self.populate_model()
        self.list_view.setModel(self.standard_item_model)
        self.selection_model = self.list_view.selectionModel()
        self.selection_model.selectionChanged.connect(self.on_selection_changed)
        list_box.addWidget(self.list_view)

        list_btn_box = QVBoxLayout()
        list_box.addLayout(list_btn_box)
        list_btn_box.addStretch(1)
        self.btn_up = QPushButton()
        self.btn_up.setIcon(util.icon(util.ICON_ARROW_UP))
        self.btn_up.clicked.connect(self.on_btn_up_clicked)
        list_btn_box.addWidget(self.btn_up)
        self.btn_down = QPushButton()
        self.btn_down.setIcon(util.icon(util.ICON_ARROW_DOWN))
        self.btn_down.clicked.connect(self.on_btn_down_clicked)
        list_btn_box.addWidget(self.btn_down)
        list_btn_box.addStretch(1)

        btn_box = QHBoxLayout()
        vbox.addLayout(btn_box)
        btn_add = QPushButton(" + ")
        btn_add.clicked.connect(self.on_btn_add_clicked)
        btn_box.addWidget(btn_add)

        self.btn_delete = QPushButton(" - ")
        self.btn_delete.clicked.connect(self.on_btn_delete_clicked)
        btn_box.addWidget(self.btn_delete)

        btn_close = QPushButton("Cancel")
        btn_close.clicked.connect(self.reject)
        btn_box.addWidget(btn_close)

        btn_ok = QPushButton("OK")
        btn_ok.setDefault(True)
        btn_ok.clicked.connect(self.accept)
        btn_box.addWidget(btn_ok)

        btn_box.addStretch(1)
        self.on_selection_changed()

    def str_list(self):
        return list(self.__str_list)

    def populate_model(self):
        self.standard_item_model.clear()
        for path in self.__str_list:
            item = QStandardItem(path)
            self.standard_item_model.appendRow(item)

    def on_selection_changed(self, selected=None, deselected=None):
        self.btn_delete.setEnabled(self.selection_model.hasSelection())
        self.btn_up.setEnabled(self.selection_model.hasSelection())
        self.btn_down.setEnabled(self.selection_model.hasSelection())

    def on_btn_delete_clicked(self):
        for item in self.selection_model.selectedIndexes():
            self.__str_list.remove(item.data())
        self.populate_model()
        self.on_selection_changed()

    def on_btn_add_clicked(self):
        dlg = QInputDialog(self)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setWindowTitle(self.windowTitle())
        dlg.setLabelText("Add to list")
        dlg.resize(300, 100)
        if dlg.exec_():
            self.insert_item(0, dlg.textValue())

    def on_btn_up_clicked(self):
        row = self.selection_model.currentIndex().row()
        if row > 0:
            self.replace_item(row, row - 1)

    def on_btn_down_clicked(self):
        row = self.selection_model.currentIndex().row()
        if row < len(self.__str_list) - 1:
            self.replace_item(row, row + 1)

    def replace_item(self, old_row, new_row):
        self.standard_item_model.insertRow(new_row, self.standard_item_model.takeRow(old_row))
        self.__str_list.insert(new_row, self.__str_list.pop(old_row))
        self.selection_model.clearSelection()
        qmodelindex = self.standard_item_model.index(new_row, 0)
        self.selection_model.setCurrentIndex(qmodelindex, QItemSelectionModel.Select)

    def insert_item(self, index, item):
        self.__str_list.insert(index, item)
        self.populate_model()

    def append_item(self, item):
        self.__str_list.append(item)
        self.populate_model()


class GPathListDialog(GListDialog):
    MODE_EXISTING_FILE = 0
    MODE_EXISTING_DIRECTORY = 1
    MODE_SAVE_FILE_NAME = 2

    def __init__(self, parent, item_list=list(), window_title="Paths", mode=MODE_EXISTING_FILE,
                 start_path=os.path.expanduser("~")):
        GListDialog.__init__(self, parent, item_list, window_title)
        self.mode = mode
        self.start_path = start_path

    def on_btn_add_clicked(self):
        if self.mode == 0:
            filename = QFileDialog.getOpenFileName(self.parent(), "Open File", self.start_path)
            if filename[0] != "":
                self.insert_item(0, filename[0])
        elif self.mode == 1:
            filename = QFileDialog.getExistingDirectory(self.parent(), "Open Folder", self.start_path)
            if filename != "":
                self.insert_item(0, filename)
        elif self.mode == 2:
            filename = QFileDialog.getSaveFileName(self.parent(), "Save File", self.start_path)
            if filename != "":
                self.insert_item(0, filename[0])
