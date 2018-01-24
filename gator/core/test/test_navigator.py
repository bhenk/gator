#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import unittest

from core import services
from core.navigator import Resources


class TestResources(unittest.TestCase):

    def test_resources(self):
        path = os.path.join(services.application_home(), "gwid", "img")
        path_list = [path]
        resources = Resources(path_list)

        self.assertEqual(1, resources.folder_count())
        print(resources.get_resource(0))


