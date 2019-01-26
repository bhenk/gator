#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import re
import shutil
import pandas as pd
from abc import abstractmethod
from datetime import datetime

from store.obj import Resource

LOG = logging.getLogger(__name__)

DATE_FORMAT = "%Y%m%d%H%M%S"


class DateStore(object):
    """
    A Store for a string and a bunch of dates. This implementation backed by a pandas.DataFrame.
    """

    def __init__(self, filename, add_once=True):
        self.filename = filename
        if os.path.exists(filename):
            self.df = pd.read_csv(filename, index_col=0, dtype={'pad': str, 'datum': str}, parse_dates=['datum'])
        else:
            self.df = pd.DataFrame(columns=['pad', 'datum'])
        self.__add_once = add_once
        self.__dated_set = set()

    @abstractmethod
    def get_dates(self, resource: Resource) -> list:
        raise NotImplementedError

    @abstractmethod
    def set_dates(self, resource: Resource, date_list: list):
        raise NotImplementedError

    @abstractmethod
    def append_date(self, resource: Resource, date: datetime):
        raise NotImplementedError

    def append_dated(self, dated: list):
        self.__dated_set.update(dated)

    def clear_dated(self):
        self.__dated_set.clear()

    def add_date_on(self, resource: Resource):
        """
        Add the current date on the given resource.
        If add_once will only do so once during the live span of this object.
        :param resource: the resource to update
        :return: None
        """
        if not(resource.filename() in self.__dated_set and self.__add_once):
            new_date = datetime.today()
            self.df = self.df.append({'pad': resource.filename(), 'datum': pd.Timestamp(new_date)}, ignore_index=True)
            len_dates = self.append_date(resource, new_date)
            self.__dated_set.add(resource.filename())
            LOG.debug("Set %s #%d on %s" % (self.__class__.__name__[:-5], len_dates, resource.filename()))

    def update(self, resource: Resource):
        """
        Update the given resource wit whatever values this store takes care for.
        :param resource: the resource to update
        :return: None
        """
        self.set_dates(resource, self.get_dates_for(resource))

    def get_dates_for(self, resource: Resource) -> list:
        """
        Get a list of dates for the given resource.
        :param resource: the resource to get the list for
        :return: list of datetime, may be empty
        """
        if len(self.df) == 0:
            date_list = []
        else:
            date_list = self.df[self.df.pad == resource.filename()].datum.dt.to_pydatetime().tolist()
        return date_list

    def resource_generator(self) -> iter:
        """
        Get a generator that yields all resources held by this store.
        :return: generator of resources
        """
        def generator() -> Resource:
            dfr = self.df.groupby('pad').size().reset_index(name='keer')
            for index, row in dfr.iterrows():
                resource = Resource(row.pad)
                self.update(resource)
                yield resource
        return generator

    def sequence_count(self, total=0):
        """
        Gives the total keer per pad in a list.
        The list is extended up to total with zero's if total greater than length of the list.
        [1, 2] with total=7 yields [1, 2, 0, 0, 0, 0, 0]
        :param total: the total
        :return: sequence
        """
        sequence = self.df.groupby('pad').size().tolist()
        x = len(sequence)
        if total > x:
            sequence.extend([0] * (total - x))
        return sequence

    def count_dates(self, filename):
        return len(self.df[self.df.pad == filename])

    def history_dataframe(self, threshold=0) -> pd.DataFrame:
        """
        returns a dataframe of [pad, keer, laatste_datum] where keer > threshold, sorted on laatste_datum.
        :param threshold: threshold for keer
        :return: dataframe
        """
        pad_grouped = self.df.groupby(self.df.pad)
        dfmax = pad_grouped.max().reset_index().rename(columns={'datum': 'laatste_datum'})
        dfkeer = pad_grouped.size().reset_index(name='keer')
        dfkeer = dfkeer[dfkeer.keer > threshold]
        return pd.merge(dfkeer, dfmax, how='inner', on='pad').sort_values(by='laatste_datum')

    def history_keys(self, threshold=0) -> []:
        """
        Get pad, sorted on latest datum, where keer > threshold
        :param threshold: threshold for keer
        :return: list of pad
        """
        return self.history_dataframe(threshold).pad.tolist()

    def save(self, path=None):
        if path is None:
            path = self.filename
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.df.to_csv(path)
        LOG.info('Saved date store %s' % path)


class AcmeDateStore(DateStore):

    def get_dates(self, resource: Resource) -> list:
        return resource.acme_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_acme_dates(date_list)

    def append_date(self, resource: Resource, date: datetime):
        resource.add_acme_date(date)
        return len(resource.acme_dates())


class ViewDateStore(DateStore):

    def get_dates(self, resource: Resource) -> list:
        return resource.view_dates()

    def set_dates(self, resource: Resource, date_list: list):
        resource.set_view_dates(date_list)

    def append_date(self, resource: Resource, date: datetime):
        resource.add_view_date(date)
        return len(resource.view_dates())


class Store(object):
    """
    Store and factory for x_store objects. A store can replicate itself.
    """

    def __init__(self, store_home):
        self.store_home = store_home
        self.__open = True
        self.stores = dict()
        self.store_names = [ViewDateStore.__name__.lower(),
                            AcmeDateStore.__name__.lower()]

    def view_date_store(self) -> ViewDateStore:
        filename = "store/%s.csv" % ViewDateStore.__name__.lower()
        if filename not in self.stores:
            vds = ViewDateStore(os.path.join(self.store_home, filename))
            self.stores[filename] = vds
        return self.stores[filename]

    def acme_date_store(self) -> AcmeDateStore:
        filename = "store/%s.csv" % AcmeDateStore.__name__.lower()
        if filename not in self.stores:
            ads = AcmeDateStore(os.path.join(self.store_home, filename))
            self.stores[filename] = ads
        return self.stores[filename]

    def close(self):
        self.view_date_store().save()
        self.acme_date_store().save()
        if self.__open:
            try:
                self.replicate()
            except Exception as err:
                LOG.error("Could not replicate", err)
            finally:
                self.__open = False
                LOG.info("##### Closed store @ %s" % self.store_home)
        else:
            LOG.warning("Trying to close a store that has already been closed.")

    def replicate(self):
        rep_dir = self._replication_dir()
        self.view_date_store().save(os.path.join(rep_dir, "viewdatestore.csv"))
        self.acme_date_store().save(os.path.join(rep_dir, "acmedatestore.csv"))
        self._cleanup(rep_dir)

    def _replication_dir(self):
        dir = os.path.dirname(self.store_home)
        date_str = datetime.today().strftime(DATE_FORMAT)
        rep_dir = os.path.join(dir, "repl", date_str)
        os.makedirs(rep_dir, exist_ok=True)
        return rep_dir

    def _cleanup(self, rep_dir):
        dir = os.path.dirname(rep_dir, )
        for rep_dir in sorted([d for d in os.listdir(dir) if re.search("^[0-9]*$", d)], reverse=True)[10:]:
            target_dir = os.path.join(dir, rep_dir)
            shutil.rmtree(target_dir)
            LOG.info("Deleted db replica %s" % target_dir)



