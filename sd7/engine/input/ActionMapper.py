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

from bootstrap.xmlparser import XMLParser
from sd7.engine.subsystem import SubSystem

__version__ = "$Revision$"

__all__ = ["ActionMapper","ActionMapperException"]


class ActionMapperException(Exception): pass


class ActionMapper(SubSystem):

    def __init__(self,options=None):
        SubSystem.__init__(self,"ActionMapper",True,options)

    def initialize(self):
        if not SubSystem.initialize(self):
            return False
        self._readDefinitions()

    def _readDefinitions(self):
        if self._config.has_key("input.actionmap"):
            fname = self._config.get("input.actionmap")
        else:
            fname = "config/input.xml"
        x = XMLParser()
        x.readfile(fname)
        




if __name__ == "__main__":
    import os
    os.chdir("../../../")

    am = ActionMapper({"input.actionmap":"config/input.xml"})
    am.initialize()



