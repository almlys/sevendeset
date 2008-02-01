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
Dictionary that preserves key order, to avoid caos at the config files
"""

__version__ = "$Revision$"

__all__ = ["MyDict"]

class MyDict(dict):

    def __init__(self):
        dict.__init__(self)
        self.__sortedlist = []
    
    def __iter__(self):
        return self.__sortedlist.__iter__()
    
    def __setitem__(self,itm,value):
        if itm not in self.__sortedlist:
            self.__sortedlist.append(itm)
        return dict.__setitem__(self,itm,value)
    
    def __delitem__(self,itm):
        self.__sortedlist.remove(itm)
        return dict.__delitem__(self,itm)
