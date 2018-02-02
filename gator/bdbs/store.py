#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from abc import abstractmethod
from datetime import datetime

from bdbs import env
from bdbs.env import BDB, Repository
from bdbs.obj import Resource

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
        self.stores = dict()

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
        self.repository.close()
        LOG.info("Closed store @ %s" % self.repository.db_home())

