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
 logger class 
"""

__version__ = "$Revision$"

__all__ = ["Mlog"]


class Mlog(object):
    def __init__(self, handle, filename, mode="w"):
        self.file = file(filename, mode)
        self.handle = handle
    def write(self,x):
        #try:
        #    self.handle.write(x.encode("utf-8"))
        #except:
        self.handle.write(x)
        #self.file.write(x.encode("utf-8"))
        if self.file.closed:
            self.handle.write("What the hell, the file is clossed!?\n")
        else:
            self.file.write(x)

    def flush(self):
        self.handle.flush()
        self.file.flush()

    def close(self):
        self.file.close()

