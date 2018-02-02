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

    def __init__(self, bdb: BDB):
        self.bdb = bdb

    @abstractmethod
    def get_dates(self, resource: Resource) -> list:
        raise NotImplementedError

    @abstractmethod
    def set_dates(self, resource: Resource, date_list: list):
        raise NotImplementedError

    def add_date_on(self, resource: Resource):
        new_date_str = datetime.today().strftime(DATE_FORMAT)
        date_str = self.bdb.get(resource.filename())
        date_str = new_date_str if date_str is None else "%s%s%s" % (date_str, env.LIST_SEP, new_date_str)
        self.bdb.put(resource.filename(), date_str)
        date_list = [datetime.strptime(string, DATE_FORMAT) for string in date_str.split(env.LIST_SEP)]
        self.set_dates(resource, date_list)

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

    def max_dates(self) -> int:
        max_dates = 0
        for value in self.bdb.values_decoded():
            date_count = len(value.split(env.LIST_SEP))
            max_dates = max(max_dates, date_count)
        return  max_dates

    def count_dates(self, filename):
        dates = self.bdb.get(filename)
        return 0 if dates is None else len(dates.split(env.LIST_SEP))


class ViewDateStore(DateStore):

    def __init__(self, bdb: BDB):
        DateStore.__init__(self, bdb)
        self.__list_viewed = []

    def get_dates(self, resource: Resource) -> list:
        return resource.view_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_view_dates(date_list)

    def add_date_on(self, resource: Resource):
        if resource.filename() in self.__list_viewed:
            return
        else:
            super().add_date_on(resource)
            self.__list_viewed.append(resource.filename())
            LOG.debug("Set view date #%d on %s" % (resource.count_view_dates(), resource.filename()))


class AcmeDateStore(DateStore):

    def get_dates(self, resource: Resource) -> list:
        return resource.acme_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_acme_dates(date_list)

    def add_date_on(self, resource: Resource):
        super().add_date_on(resource)
        LOG.debug("Set acme date #%d on %s" % (resource.count_acme_dates(), resource.filename()))


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

