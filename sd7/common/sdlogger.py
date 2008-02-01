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

__all__ = ["mlog"]


class mlog(object):
    def __init__(self,handle,filename,mode="w"):
        self.file=file(filename,mode)
        self.handle=handle
    def write(self,x):
        self.handle.write(x.encode("utf-8"))
        self.file.write(x.encode("utf-8"))
    def flush():
        self.handle.flush()
        self.file.flush()
    def close(self):
        self.file.close()

