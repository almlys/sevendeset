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
Example file, with basic Input that handles input action 'exit'
"""

__version__ = "$Revision$"

__all__ = ["MyBasicInputHandler"]

from sd7.engine.controller import Controller
from sd7.engine.Events import EventType
from sd7.engine.Engine import Engine

class MyBasicInputHandler(Controller):
    
    def __init__(self,params):
        Controller.__init__(self,params)

    def initialize(self):
        Controller.initialize(self)

    def processEvent(self,evt):
        if evt.getType() == EventType.ACTION_DOWN:
            if evt.getObject().name == "exit":
                self.log("Terminating the Engine by user script")
                Engine().terminate()
        
