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
    #Input events
    KEY_PRESSED = 6
    KEY_RELEASED = 7
    MOUSE_MOVED = 8
    MOUSE_PRESSED = 9
    MOUSE_RELEASED = 10
    #Action Event
    ACTION_DOWN  = 11
    ACTION_UP = 12
    ACTION_AXIS = 13
    
    stype = ["WIN_CLOSED","WIN_MOVED","WIN_RESIZED","WIN_FOCUS","FRAME_STARTED",
    "FRAME_ENDED","KEY_PRESSED","KEY_RELEASED","MOUSE_MOVED","MOUSE_PRESSED",
    "MOUSE_RELEASED","ACTION_DOWN","ACTION_UP","ACTION_AXIS"]


def toString(type):
    return EventType.stype[type]


class Event(object):
    
    def __init__(self,type,object):
        self._type = type
        self._object = object
    
    def getType(self):
        return self._type
    
    def getObject(self):
        return self._object

    def __str__(self):
        return "Event type: %i, %s, %s" %(self._type,toString(self._type),str(self.getObject()))
