#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import shutil
import sys
import unittest

from store.store import Store
from core.navigator import Universe, DefaultPilot, Navigator


class TestDefaultPilot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # logging:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

    def setUp(self):
        self.db_home = os.path.abspath("navigator_test")
        shutil.rmtree(self.db_home, ignore_errors=True)
        self.store = Store(self.db_home)
        self.universe = Universe([])

    def test_pilot_in_empty_universe(self):
        pilot = DefaultPilot(self.store, self.universe)

        self.assertEqual((0, 0), pilot.space())
        self.assertEqual(0, pilot.space_x())
        self.assertEqual(0, pilot.space_y())
        self.assertEqual(0, pilot.index_x())

        resource1 = pilot.current_resource()

        self.assertEqual(-1, resource1.index())
        self.assertIsNone(resource1.filename())

        self.assertEqual(-1, pilot.universe_index())
        self.assertIsNone(pilot.filename())
        self.assertEqual((1, 0), pilot.space())
        self.assertEqual(1, pilot.space_x())
        self.assertEqual(0, pilot.space_y())

        self.assertEqual(0, pilot.index_x())

        resource2 = pilot.go_up()
        self.assertEqual(resource1, resource2)
        resource3 = pilot.go_down()
        self.assertEqual(resource2, resource3)
        resource4 = pilot.go_left()
        self.assertEqual(resource3, resource4)
        resource5 = pilot.go_right()
        self.assertEqual(resource4, resource5)
        resource6 = pilot.go_start()
        self.assertEqual(resource5, resource6)

        self.assertEqual(0, pilot.start_index())


class TestNavigator(unittest.TestCase):

    def setUp(self):
        self.db_home = os.path.abspath("navigator_test")
        shutil.rmtree(self.db_home, ignore_errors=True)
        self.store = Store(self.db_home)
        self.universe = Universe([])

    def test_navigator(self):
        navigator = Navigator(self.store, self.universe)

        print(navigator.pilots["Default"])

        #print(navigator.pilots["Default"](self.store, self.universe))



