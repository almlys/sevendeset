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

__all__ = ["GUI"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class GUI(Controller):

    __name__ = "GUI"
    _params = {}
    
    def __init__(self,params):
        Controller.__init__(self,params)
        self._params = params

    def initialize(self):
        Controller.initialize(self)
        self.log("Initializing %s" %(self.__name__))

        # get the GUI and load the chat View
        self._gui = Engine().getGUI()
        self._gui.loadView(self._params["layout"])
        # Watch for input events
        #self._gui.subscribeEvent("Chat/ChatWindow/ChatOkBtn",
        #    self._gui.getEvent("PushButton/EventClicked"),self.onInput)
    
        #self._gui.getObject("Chat/ChatWindow/ChatBox").setText("Connection code is missing")
    
        # get Net and watch for incomming messages
        #self._net = wathever
        #self._net.subscribeMsg("chat,",self.onMsg)

