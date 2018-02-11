#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import logging
import operator
import os
import re
import shutil
from abc import abstractmethod
from datetime import datetime

from bdbs import env
from bdbs.env import BDB, Repository
from bdbs.obj import Resource
from core.services import NlDialect

LOG = logging.getLogger(__name__)

DATE_FORMAT = "%Y%m%d%H%M%S"


class DateStore(object):

    def __init__(self, bdb: BDB, add_once=True):
        self.bdb = bdb
        self.__add_once = add_once
        self.__dated_set = set()

    @abstractmethod
    def get_dates(self, resource: Resource) -> list:
        raise NotImplementedError

    @abstractmethod
    def set_dates(self, resource: Resource, date_list: list):
        raise NotImplementedError

    def append_dated(self, dated: list):
        self.__dated_set.update(dated)

    def clear_dated(self):
        self.__dated_set.clear()

    def add_date_on(self, resource: Resource):
        if not(resource.filename() in self.__dated_set and self.__add_once):
            new_date_str = datetime.today().strftime(DATE_FORMAT)
            date_str = self.bdb.get(resource.filename())
            date_str = new_date_str if date_str is None else "%s%s%s" % (date_str, env.LIST_SEP, new_date_str)
            self.bdb.put(resource.filename(), date_str)
            date_list = [datetime.strptime(string, DATE_FORMAT) for string in date_str.split(env.LIST_SEP)]
            self.set_dates(resource, date_list)
            self.__dated_set.add(resource.filename())
            LOG.debug("Set %s #%d on %s" % (self.__class__.__name__[:-5], len(date_list), resource.filename()))

    def update(self, resource: Resource):
        self.set_dates(resource, self.get_dates_for(resource))

    def get_dates_for(self, resource: Resource) -> list:
        date_str_list = self.bdb.get_list(resource.filename(), default=list())
        return [datetime.strptime(string, DATE_FORMAT) for string in date_str_list]

    def resource_generator(self) -> iter:
        def generator() -> Resource:
            for item in self.bdb.items_decoded():
                resource = Resource(item[0])
                date_list = [datetime.strptime(string, DATE_FORMAT) for string in item[1].split(env.LIST_SEP)]
                self.set_dates(resource, date_list)
                yield resource
        return generator

    def sequence_count(self, total=0):
        sequence = []
        for value in self.bdb.values_decoded():
            date_count = len(value.split(env.LIST_SEP))
            sequence.append(date_count)
        x = len(sequence)
        if total > x:
            sequence.extend([0] * (total - x))
        return sequence

    def count_dates(self, filename):
        dates = self.bdb.get(filename)
        return 0 if dates is None else len(dates.split(env.LIST_SEP))

    def history_items(self, threshold=0) -> [()]:
        latest = self.bdb.get_keys_with_latest_values(threshold)
        return sorted(latest.items(), key=operator.itemgetter(1))

    def history_keys(self, threshold=0) -> []:
        return [item[0] for item in self.history_items(threshold)]


class AcmeDateStore(DateStore):

    def get_dates(self, resource: Resource) -> list:
        return resource.acme_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_acme_dates(date_list)


class ViewDateStore(DateStore):

    def get_dates(self, resource: Resource) -> list:
        return resource.view_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_view_dates(date_list)


class Store(object):

    def __init__(self, db_home):
        self.repository = Repository(db_home)
        self.__open = True
        self.stores = dict()
        self.store_names = [ViewDateStore.__name__.lower(),
                            AcmeDateStore.__name__.lower()]

    def view_date_store(self) -> ViewDateStore:
        filename = "store/%s.bdb" % ViewDateStore.__name__.lower()
        if filename not in self.stores:
            vds = ViewDateStore(self.repository.bdb(filename, cache=False))
            self.stores[filename] = vds
        return self.stores[filename]

    def acme_date_store(self) -> AcmeDateStore:
        filename = "store/%s.bdb" % AcmeDateStore.__name__.lower()
        if filename not in self.stores:
            ads = AcmeDateStore(self.repository.bdb(filename, cache=False))
            self.stores[filename] = ads
        return self.stores[filename]

    def close(self):
        if self.__open:
            try:
                self.replicate()
            except Exception as err:
                LOG.error("Could not replicate", err)
            finally:
                self.repository.close()
                self.__open = False
                LOG.info("##### Closed store @ %s" % self.repository.db_home())
        else:
            LOG.warning("Trying to close a store that has already been closed.")

    def replicate(self):
        rep_dir = self._replication_dir()
        for name in self.store_names:
            self._replicate_bdb(self.view_date_store().bdb, rep_dir, name + ".csv")
        self._cleanup(rep_dir)

    def _replication_dir(self):
        dir = os.path.dirname(self.repository.db_home())
        date_str = datetime.today().strftime(DATE_FORMAT)
        rep_dir = os.path.join(dir, "repl", date_str)
        os.makedirs(rep_dir, exist_ok=True)
        return rep_dir

    def _replicate_bdb(self, bdb, rep_dir, name):
        filename = os.path.join(rep_dir, name)
        with open(filename, "w", encoding="UTF-8") as f:
            writer = csv.writer(f, dialect=NlDialect)
            for item in bdb.items_decoded():
                writer.writerow([item[0], item[1]])
        LOG.info("Replicated %s" % filename)

    def _cleanup(self, rep_dir):
        dir = os.path.dirname(rep_dir, )
        for rep_dir in sorted([d for d in os.listdir(dir) if re.search("^[0-9]*$", d)], reverse=True)[10:]:
            target_dir = os.path.join(dir, rep_dir)
            shutil.rmtree(target_dir)
            LOG.info("Deleted db replica %s" % target_dir)



