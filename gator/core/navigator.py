#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import random

from bdbs.obj import Resource
from bdbs.store import Store
from core.services import Format, Stat

LOG = logging.getLogger(__name__)

EXTENSIONS = ['.jpg', '.bmp', '.png', '.gif']


class Universe(object):

    @staticmethod
    def filter_list():
        return "Images(*%s)" % " *".join(EXTENSIONS)

    def __init__(self, path_list=list()):
        self.__path_list = path_list
        self.__filename_list = list()
        self.__folder_list = list()
        self.__init_lists__()

    def __init_lists__(self):
        for path in self.__path_list:
            for (dir_path, dir_names, filenames) in os.walk(path):
                for fn in filenames:
                    if os.path.splitext(fn)[1].lower() in EXTENSIONS:
                        self.__filename_list.append(os.path.join(dir_path, fn))
                        if dir_path not in self.__folder_list:
                            self.__folder_list.append(dir_path)

    def size(self) -> int:
        return len(self.__filename_list)

    def path_list(self) -> list:
        return list(self.__path_list)

    def filename_list(self) -> list:
        return list(self.__filename_list)

    def folder_list(self) -> list:
        return list(self.__folder_list)

    def common_prefix(self) -> str:
        return os.path.dirname(os.path.commonprefix(self.__folder_list))

    def paths_count(self) -> int:
        return len(self.__path_list)

    def filename_count(self) -> int:
        return len(self.__filename_list)

    def folder_count(self) -> int:
        return len(self.__folder_list)

    def to_string(self) -> str:
        return "filenames: %s  |  folders: %s  |  paths: %s" % (
            Format.decimal(self.filename_count()),
            Format.decimal(self.folder_count()),
            Format.decimal(self.paths_count()))

    def filename_by_index(self, index) -> str or None:
        if index < 0 or index > self.filename_count() - 1:
            return None
        else:
            return self.__filename_list[index]

    def index(self, filename) -> int:
        if filename in self.__filename_list:
            return self.__filename_list.index(filename)
        else:
            return -1


class Pilot(object):
    """
    A :class:`Pilot` is able to travel in a :class:`Universe` and pick up :class:`Resource`\ s.
    """

    def __init__(self, store: Store, universe: Universe):
        self._store = store
        self._universe = universe
        self._universe_index = -1
        self._filename = None

    def space(self) -> (int, int):
        """
        Return the space this pilot can travel expressed as space.x, space.y

        :return: (space.x, space.y)
        """
        return -1, -1

    def space_x(self):
        """
        The depth of a :class:`Pilot`\ 's space in :class:`Resource`\ s.

        :return: depth of a :class:`Pilot`\ 's space
        """
        return self.space()[0]

    def space_y(self):
        """
        The width of a :class:`Pilot`\ 's space in :class:`Resource`\ s.

        :return: width of a :class:`Pilot`\ 's space
        """
        return self.space()[1]

    def stat(self) -> Stat:
        return Stat([])

    def universe_index(self) -> int:
        return self._universe_index

    def index_x(self):
        return -1

    def filename(self) -> str:
        return self._filename

    def current_resource(self) -> Resource or None:
        return None

    def go_start(self) -> Resource or None:
        return None

    def go_up(self) -> Resource or None:
        return None

    def go_down(self) -> Resource or None:
        return None

    def go_left(self) -> Resource or None:
        return None

    def go_right(self) -> Resource or None:
        return None

    def _create_resource_by_index(self, index) -> Resource or None:
        filename = self._universe.filename_by_index(index)
        return self._create_resource(index, filename)

    def _create_resource_by_filename(self, filename):
        index = self._universe.index(filename)
        return self._create_resource(index, filename)

    def _create_resource(self, index=-1, filename=None):
        if index < 0 or filename is None:
            index = self._universe_index
            filename = self._filename
        resource = Resource(filename, index)
        self._store.acme_date_store().update(resource)
        self._store.view_date_store().update(resource)
        self._universe_index = index
        self._filename = filename
        return resource


class DefaultPilot(Pilot):

    def __init__(self, store: Store, universe: Universe):
        Pilot.__init__(self, store, universe)
        self.__size_y = self._universe.size()
        stat = self.stat()
        self.__min_views = stat.min()
        LOG.info("view stats: %s" % stat.to_string(join=" | "))

        self.__resource = self._create_resource(*self._random_()[0:2])

        self.__history_list = self._store.view_date_store().history_keys(self.__min_views)
        self._store.view_date_store().append_dated(self.__history_list)
        if len(self.__history_list) >= self.__size_y:
            self.__history_list.clear()
            self._store.view_date_store().clear_dated()
            LOG.info("Cleared history list")
        self.__history_index = len(self.__history_list)
        self.__start_index = self.__history_index

    def set_filename(self, filename: str):
        if filename and filename in self._universe.filename_list():
            self.__resource = self._create_resource_by_filename(filename)

    def space(self) -> (int, int):
        return len(self.__history_list), self.__size_y

    def index_x(self):
        return self.__history_index

    def start_index(self):
        return self.__start_index

    def stat(self) -> Stat:
        return Stat(self._store.view_date_store().sequence_count(total=self.__size_y))

    def current_resource(self):
        return self._append_history(self.__resource)

    def go_start(self):
        return self._history_resource(self.__start_index)

    def go_up(self):
        return self._history_resource(self.__history_index - 1)

    def go_down(self):
        return self._history_resource(self.__history_index + 1)

    def go_left(self):
        return self._universe_resource(self._universe_index - 1)

    def go_right(self):
        return self._universe_resource(self._universe_index + 1)

    def _random_(self) -> (int, str):
        if self.__size_y > 0:
            idx = random.randint(0, self.__size_y - 1)
            filename = self._universe.filename_by_index(idx)
            views = self._store.view_date_store().count_dates(filename)
            tries = 0
            while views > self.__min_views:
                tries += 1
                idx += 1
                if idx >= self.__size_y:
                    idx = 0
                    LOG.debug("Recalculating min views")
                    minimal_views = self.stat().min()
                    if minimal_views != self.__min_views:
                        LOG.info("Adjusting min views to %d" % minimal_views)
                        self.__min_views = minimal_views

                filename = self._universe.filename_by_index(idx)
                views = self._store.view_date_store().count_dates(filename)

            if tries > 0:
                LOG.debug("Found filename after %d tries. __min_views=%d" % (tries, self.__min_views))
            return idx, filename
        else:
            return -1, None

    def _append_history(self, resource: Resource) -> Resource:
        if not resource.filename() in self.__history_list:
            self.__history_list.append(resource.filename())
        return resource

    def _history_resource(self, history_index: int) -> Resource:
        self.__history_index = history_index
        if self.__history_index < 0:
            self.__history_index = 0
        if self.__history_index >= len(self.__history_list):
            idx, filename = self._random_()
            self.__history_list.append(filename)
        if self.__history_index >= len(self.__history_list):
            self.__history_index = len(self.__history_list) - 1

        filename = self.__history_list[self.__history_index]
        if self.__resource.filename() != filename:
            self.__resource = self._create_resource_by_filename(filename)
        return self._append_history(self.__resource)

    def _universe_resource(self, universe_index: int) -> Resource:
        self._universe_index = universe_index
        if self._universe_index < 0:
            self._universe_index = 0
        if self._universe_index >= self._universe.size():
            self._universe_index = self._universe.size() - 1

        resource = self._create_resource_by_index(self._universe_index)
        if self.__resource.filename() != resource.filename():
            self.__resource = resource
        return self._append_history(self.__resource)


class AcmePilot(Pilot):

    def __init__(self, store: Store, universe: Universe):
        Pilot.__init__(self, store, universe)
        self.__acme_list = self._store.acme_date_store().history_keys()
        self.__acme_index = len(self.__acme_list)
        self.__start_index = self.__acme_index
        self.__size_y = len(self.__acme_list)
        sequence = self._store.acme_date_store().sequence_count(total=self.__size_y)
        stat = Stat(sequence)
        LOG.info("acme stats: %s" % stat.to_string(join=" | "))
        self.__resource = None
        self.__resource = self._acme_resource(self.__acme_index)

    def space(self) -> (int, int):
        return self.__size_y, self.__size_y

    def index_x(self):
        return self.__acme_index

    def start_index(self):
        return self.__start_index

    def stat(self) -> Stat:
        return Stat(self._store.acme_date_store().sequence_count(total=self.__size_y))

    def current_resource(self):
        return self.__resource

    def go_start(self):
        return self._acme_resource(self.__start_index)

    def go_up(self):
        return self._acme_resource(self.__acme_index - 1)

    def go_down(self):
        return self._acme_resource(self.__acme_index + 1)

    def go_left(self):
        filename_acme = self.__acme_list[self.__acme_index]
        idx = self._universe.index(filename_acme) - 1
        print("start universe index", idx)

        for filename in self._universe.filename_list()[idx::-1]:
            print(self._universe.index(filename), filename)
            if filename in self.__acme_list:
                self.__acme_index = self.__acme_list.index(filename)
                break
        return self._acme_resource(self.__acme_index)

    def go_right(self):
        filename_acme = self.__acme_list[self.__acme_index]
        idx = self._universe.index(filename_acme) + 1

        for filename in self._universe.filename_list()[idx::1]:
            if filename in self.__acme_list:
                self.__acme_index = self.__acme_list.index(filename)
                break
        return self._acme_resource(self.__acme_index)

    def _acme_resource(self, acme_index) -> Resource:
        self.__acme_index = acme_index
        if self.__acme_index < 0:
            self.__acme_index = 0;
        if self.__acme_index >= len(self.__acme_list):
            self.__acme_index = len(self.__acme_list) - 1

        filename = None if self.__acme_index < 0 else self.__acme_list[self.__acme_index]
        if self.__resource is None or self.__resource.filename() != filename:
            self.__resource = self._create_resource_by_filename(filename)
        return self.__resource


class Navigator(object):

    PILOTS = ["Default", "Acme"]

    def __init__(self, store: Store, universe=Universe(), filename=None):
        self.__store = store
        self.__universe = universe
        self.pilots = {}
        self.pilot = DefaultPilot(store, universe)
        self.pilot.set_filename(filename)
        self.pilots[Navigator.PILOTS[0]] = self.pilot

    def set_pilot(self, pilot_name: str=None, pilot_index: int=-1):
        if pilot_index >= 0:
            pilot_name = Navigator.PILOTS[pilot_index]
        if pilot_name in Navigator.PILOTS:
            if not pilot_name in self.pilots.keys():
                self.pilots[pilot_name] = self._create_pilot(pilot_name)
            self.pilot = self.pilots[pilot_name]

    def space(self) -> (int, int):
        return self.pilot.space()

    def stat(self)-> Stat:
        return self.pilot.stat()

    def index_x(self):
        return self.pilot.index_x()

    def is_at_start(self):
        return self.pilot.index_x() == self.pilot.start_index()

    def current_resource(self) -> Resource:
        return self.pilot.current_resource()

    def go_history_start(self):
        return self.pilot.go_start()

    def go_start(self):
        return self.pilot.go_start()

    def go_history_end(self):
        return self.pilot.go_start()

    def go_down(self):
        return self.pilot.go_down()

    def go_up(self):
        return self.pilot.go_up()

    def go_left(self):
        return self.pilot.go_left()

    def go_right(self):
        return self.pilot.go_right()

    def _create_pilot(self, name: str):
        if name == Navigator.PILOTS[0]:
            return DefaultPilot(self.__store, self.__universe)
        elif name == Navigator.PILOTS[1]:
            return AcmePilot(self.__store, self.__universe)
