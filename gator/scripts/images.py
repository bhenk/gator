#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import inspect
import os

from gwid.util import GIcon


def list_used_images():
    images = list()
    for x in inspect.getmembers(GIcon):
        if inspect.isfunction(x[1]):
            print(x[0], x[1].__code__.co_consts[1])
            images.append(x[1].__code__.co_consts[1])
    return images


def remove_images(remain=None):
    count = 0
    img_dir = "../img"
    for file in os.listdir(img_dir):
        if remain and file not in remain:
            count += 1
            print("removing", file)
            os.remove(os.path.join(img_dir, file))
    return count


if __name__ == '__main__':
    used_images = list_used_images()
    used_images.append("gator.icns")
    count_removed = remove_images(used_images)
    print()
    print("used  images:", len(used_images))
    print("total images:", len(os.listdir("../img")))
    print("images removed:", count_removed)