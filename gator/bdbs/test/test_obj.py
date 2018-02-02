#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from datetime import datetime

from bdbs.obj import Resource


class TestResource(unittest.TestCase):

    def test_null_filename(self):
        resource = Resource()
        self.assertIsNone(resource.filename())
        self.assertIsNone(resource.basename())
        self.assertIsNone(resource.slv_index())
        self.assertIsNone(resource.short_name())
        self.assertIsNone(resource.long_name())

    def test_dates_formatted(self):
        resource = Resource()
        date_list = [datetime.today(), datetime.today(), datetime.today()]
        resource.set_acme_dates(date_list)
        print(resource.acme_dates())
        print(resource.acme_dates(fmt="%Y-%m-%d"))
        print("\n".join(resource.acme_dates(fmt="%Y-%m-%d")))

