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

from sd7.engine.Engine import Engine
from sd7.engine.controller import Controller

class MyBasicInputHandler(Controller):

    def __init__(self,params):
        Controller.__init__(self,params)
        self._guiFocus = False

    def initialize(self):
        Controller.initialize(self)
        self.toggleGUIFocus(False)


    def toggleGUIFocus(self, wtf=None):
        if wtf != None:
            self._guiFocus = wtf
        gui = Engine().getGUI()
        gui.toggleMouse(self._guiFocus)
        gui.toggleKeyboard(self._guiFocus)
        gui.toggleFocus(self._guiFocus)
        self._guiFocus = not self._guiFocus


    def onAction(self,name,down=True):
        #print self._guiFocus, name, down
        if down:
            if name == "exit":
                self.log("Terminating the Engine by user script")
                Engine().terminate()
                return True
            elif name == "gui":
                self.toggleGUIFocus()
                return True
        return False
