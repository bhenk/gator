#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='gator',
    #version=version.__version__,
    packages=['app', 'core'],
    url='https://anhenet.nl',
    license='Apache License 2.0',
    author='henk van den berg',
    description='Application for viewing images',
    install_requires=['pyqt5', 'exifread']
)