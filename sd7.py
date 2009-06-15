#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project Engine
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#

"""
Template file
"""

__version__ = "$Revision$"

__all__ = []

def runEngine():
    from sd7 import sd7Engine
    sd7Engine.runsd7()

def setUpPaths():
    import os, sys

    def setEnv(key, val, sep = ":"):
        aux = ""
        if os.environ.has_key(key):
            aux = sep + os.environ[key]
        os.environ[key] = val + aux

    if os.environ.has_key("BE_CAREFULL_ABOUT_THE_LOOP"):
        return
    os.environ["BE_CAREFULL_ABOUT_THE_LOOP"] = "I KNOW"

    version = sys.version_info
    version = str(version[0]) + "." + str(version[1])

    prefix = "runtime"
    setEnv('PATH', prefix + '/lib')
    setEnv('LD_LIBRARY_PATH', prefix + '/lib')
    setEnv('PYTHONPATH',
        os.getcwd() + ":" + prefix + '/lib/python' + \
        version + '/site-packages')
    sys.path.insert(0,os.getcwd())
    sys.path.insert(0,prefix + "/lib/python" + version + \
        "/site-packages")

    if os.fork() == 0:
        os.execv(sys.argv.pop(0), sys.argv)
    else:
        sys.exit()


def callBootStrap():
    pass

def downloadBootStrap():
    pass


if __name__ == "__main__":

    stuff_to_do = [setUpPaths, callBootStrap, downloadBootStrap]

    while len(stuff_to_do) != 0:
        try:
            runEngine()
            break
        except ImportError,e:
            print e
            stuff_to_do.pop(0)()

