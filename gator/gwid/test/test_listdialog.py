#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

from gwid.listdialog import GListDialog, GPathListDialog


class TestWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(250, 150)
        self.setWindowTitle('Test')
        hbl = QHBoxLayout(self)

        btn = QPushButton("...")
        btn.clicked.connect(self.on_btn_clicked)
        hbl.addWidget(btn)
        hbl.addStretch(1)

        self.show()

    def on_btn_clicked(self):
        #self.test_glist_dialog()
        self.test_gpath_list_dialog()

    def test_glist_dialog(self):
        gld = GListDialog(self, ["a", "b", "c"], window_title="Testing")
        gld.deleteLater()
        if gld.exec():
            str_list = gld.str_list()
            print(str_list)

    def test_gpath_list_dialog(self):
        pld = GPathListDialog(self, [], mode=GPathListDialog.MODE_SAVE_FILE_NAME)
        pld.deleteLater()
        # pld.append_item("bla")
        if pld.exec():
            str_list = pld.str_list()
            print(str_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = TestWidget()
    sys.exit(app.exec_())

