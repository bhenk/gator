#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from bdbs import env
from bdbs.env import BDB, Repository
from bdbs.obj import Resource

LOG = logging.getLogger(__name__)

DATE_FORMAT = "%Y%m%d%H%M%S"


class ViewDateStore(object):

    def __init__(self, bdb: BDB):
        self.bdb = bdb
        self.__list_viewed = []

    def set_viewed(self, resource: Resource):
        if resource.filename() not in self.__list_viewed:
            vd_strings = self.bdb.get_list(resource.filename(), default=list())
            vd_strings.append(datetime.today().strftime(DATE_FORMAT))
            self.bdb.put_list(resource.filename(), vd_strings)
            vd = [datetime.strptime(string, DATE_FORMAT) for string in vd_strings]
            resource.set_view_dates(vd)
            self.__list_viewed.append(resource.filename())
            LOG.debug("Set view date on %s" % resource.filename())

    def update(self, resource: Resource):
        vd_strings = self.bdb.get_list(resource.filename(), default=list())
        vd = [datetime.strptime(string, DATE_FORMAT) for string in vd_strings]
        resource.set_view_dates(vd)

    def get(self, resource: Resource):
        vd_strings = self.bdb.get_list(resource.filename())
        return [datetime.strptime(string, DATE_FORMAT) for string in vd_strings]

    def resource_generator(self) -> iter:

        def generator() -> Resource:
            for item in self.bdb.items_decoded():
                resource = Resource(item[0])
                vd = [datetime.strptime(string, DATE_FORMAT) for string in item[1].split(env.LIST_SEP)]
                resource.set_view_dates(vd)
                yield resource

        return generator

    def max_views(self) -> int:
        max_views = 0
        for value in self.bdb.values_decoded():
            views = len(value.split(env.LIST_SEP))
            max_views = max(max_views, views)
        return max_views

    def count_views(self, filename):
        value = self.bdb.get(filename)
        return 0 if value is None else len(value.split(env.LIST_SEP))


class Store(object):

    def __init__(self, db_home):
        self.repository = Repository(db_home)
        self.stores = dict()

    def view_date_store(self) -> ViewDateStore:
        filename = "store/%s.bdb" % ViewDateStore.__name__.lower()
        if filename not in self.stores:
            vds = ViewDateStore(self.repository.bdb(filename))
            self.stores[filename] = vds
        return self.stores[filename]

    def close(self):
        self.repository.close()
        LOG.info("Closed store @ %s" % self.repository.db_home())

