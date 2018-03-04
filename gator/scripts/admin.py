#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from bdbs import store, env
from bdbs.store import Store
from core.services import NlDialect


def insert_dates():
    filename = "/Volumes/Backup/20171217/quinter/log.txt"
    store_db = "/Volumes/Backup/20171217/gator2/db"
    read_format = "%Y-%m-%d"

    _store = Store(store_db)
    date_store = _store.acme_date_store()

    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 1:
                ins_date = datetime.strptime(row[0], read_format)
                ins_date_str = ins_date.strftime(store.DATE_FORMAT)
                old_date_str = date_store.bdb.get(row[1])
                date_str = ins_date_str if old_date_str is None else "%s%s%s" % (ins_date_str, env.LIST_SEP, old_date_str)
                # date_store.bdb.put(row[1], date_str)
                print(date_str, row[1])


def restore_date_stores():
    # throw away the database. find proper backup files:
    view_back_up = "/Volumes/Backup/20171217/gator2/repl/20180302094400/viewdatestore.csv"
    acme_back_up = "/Volumes/Backup/20171217/gator2/repl/20180302094400/acmedatestore.csv"

    store_db = "/Volumes/Backup/20171217/gator2/db"
    _store = Store(store_db)

    date_store = _store.view_date_store()
    with open(view_back_up, "r", encoding="UTF-8") as f:
        reader = csv.reader(f, dialect=NlDialect)
        for row in reader:
            date_store.bdb.put(row[0], row[1])

    date_store = _store.acme_date_store()
    with open(acme_back_up, "r", encoding="UTF-8") as f:
        reader = csv.reader(f, dialect=NlDialect)
        for row in reader:
            date_store.bdb.put(row[0], row[1])



if __name__ == '__main__':
    # insert_dates()
    # restore_date_stores()
    pass