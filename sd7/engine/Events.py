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
Events file
"""

__version__ = "$Revision$"

__all__ = ['Event']

class EventType(object):
    WIN_CLOSED = 0
    WIN_MOVED = 1
    WIN_RESIZED = 2
    WIN_FOCUS = 3
    FRAME_STARTED = 4
    FRAME_ENDED = 5


class Event(object):
    
    def __init__(self,type,object):
        self._type = type
        self._object = object
    
    def getType(self):
        return self._type
    
    def getObject(self):
        return self._object


