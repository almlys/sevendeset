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

#NOOO
import ogre.io.OIS as OIS

class MyBasicInputHandler(Controller):
    
    def __init__(self,engine):
        self._engine = engine

    def processEvents(self,evt):
        if evt.getType() == EventType.KEY_PRESSED:
            if evt.getObject().key == OIS.KC_ESCAPE:
                self._engine.Terminate()
        
    def onInputAction(self,action,args=None):
        
        if action=="exit":
            self._engine.Terminate()
        else:
            return False
        return True
