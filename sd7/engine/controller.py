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

__all__ = ['Controller',]

from sd7.engine.Events import EventType

class Controller(object):

    _params = {}
    _initialized = False #: Is initialized?
    _debugmsg = True
    __logFunc = None
    _view = None
    
    def __init__(self, params = None):
        if params!=None:
            self._params = params
        if params.has_key("debug"):
            self._debugmsg = params["debug"]

    def log(self,msg):
        if self._debugmsg and not self.__logFunc==None:
            self.__logFunc(self.__class__.__name__ + ":" + msg)

    def setLogFunc(self,log):
        self.__logFunc = log

    def register(self,who):
        self._view = who

    def processEvent(self,evt):
        return False
        if evt.getType() == EventType.FRAME_STARTED or \
        evt.getType() == EventType.FRAME_ENDED or \
        evt.getType() == EventType.MOUSE_MOVED:
            return False
        self.log("Unprocessed event " + str(evt))
        return False

    def initialize(self):
        pass
    
    
