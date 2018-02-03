#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os

from bsddb3 import db
from bsddb3.dbobj import DB, DBEnv

LOG = logging.getLogger(__name__)

LIST_SEP = "\0"


class BDB(DB):

    def __init__(self, db_env, flags=0):
        DB.__init__(self, db_env, flags)

    @staticmethod
    def __encode(value):
        return None if value is None else value.encode("utf-8")

    @staticmethod
    def __decode(value):
        return None if value is None else value.decode("utf-8")

    def append(self, data, txn=None) -> int:
        return super().append(self.__encode(data), txn)

    def delete(self, key, txn=None, flags=0):
        super().delete(self.__encode(key), txn, flags)

    def get(self, key, default=None, txn=None, flags=0, dlen=-1, doff=-1) -> str:
        return self.__decode(super().get(self.__encode(key), self.__encode(default), txn, flags, dlen, doff))

    def get_both(self, key, data, txn=None, flags=0) -> str:
        return self.__decode(super().get_both(self.__encode(key), self.__encode(data), txn, flags))

    def get_size(self, key, txn=None) -> int:
        return super().get_size(self.__encode(key), txn)

    def key_range(self, key, txn=None, flags=0):
        return super().key_range(self.__encode(key), txn, flags)

    def has_key(self, key, txn=None):
        return super().has_key(self.__encode(key), txn)

    def pget(self, key, default=None, txn=None, flags=0, dlen=-1, doff=-1) -> str:
        return self.__decode(super().pget(self.__encode(key), self.__encode(default), txn, flags, dlen, doff))

    def put(self, key, data, txn=None, flags=0, dlen=-1, doff=-1) -> int:
        return super().put(self.__encode(key), self.__encode(data), txn, flags, dlen, doff)

    def items_decoded(self, txn=None) -> [()]:
        return [(self.__decode(tup[0]), self.__decode(tup[1])) for tup in super().items(txn)]

    def keys_decoded(self, txn=None) -> []:
        return [self.__decode(key) for key in super().keys(txn)]

    def values_decoded(self, txn=None) -> []:
        return [self.__decode(value) for value in super().values(txn)]

    def get_list(self, key, default=None, txn=None, flags=0, dlen=-1, doff=-1):
        value = self.get(key, txn=txn, flags=flags, dlen=dlen, doff=doff)
        if value:
            return value.split(LIST_SEP)
        else:
            return default

    def put_list(self, key, data, txn=None, flags=0, dlen=-1, doff=-1):
        value = LIST_SEP.join(data)
        self.put(key, value, txn, flags, dlen, doff)


class Repository(object):

    def __init__(self, db_home):
        LOG.info("db full version: %s" % str(db.full_version()))
        self.__db_home = os.path.abspath(db_home)
        os.makedirs(self.__db_home, exist_ok=True)
        self.__db_env = DBEnv()
        self.__db_env.open(self.__db_home, db.DB_INIT_MPOOL | db.DB_CREATE)
        self.__databases = dict()

    def db_home(self) -> str:
        return self.__db_home

    def db_env(self) -> DBEnv:
        return self.__db_env

    def bdb(self, filename, cache=True) -> BDB:
        if filename not in self.__databases:
            os.makedirs(os.path.dirname(os.path.join(self.__db_home, filename)), exist_ok=True)
            bdb = BDB(self.__db_env)
            bdb.open(filename, None, db.DB_BTREE, db.DB_CREATE)
            if cache:
                self.__databases[filename] = bdb
        else:
            bdb = self.__databases[filename]
        return bdb

    def close(self):
        for bdb in self.__databases.values():
            bdb.close()
        self.__db_env.close(db.DB_FORCESYNC)





