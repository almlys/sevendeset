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

__all__ = ["ChatApp"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class ChatApp(Controller):
    
    __name__ = "Chat"
    
    def __init__(self,params):
        Controller.__init__(self,params)
        print "Init chat app"
        print params

    def initialize(self):
        Controller.initialize(self)
        self.log("Initializing %s" %(self.__name__))

        # get the GUI and load the chat View
        self._gui = Engine().getGUI()
        self._gui.loadView("chat.layout")
        # Watch for input events
        self._gui.subscribeEvent("Chat/ChatWindow/ChatOkBtn",
            self._gui.getEvent("PushButton/EventClicked"),self.onInput)
    
        self._gui.getObject("Chat/ChatWindow/ChatBox").setText("Connection code is missing")
    
        # get Net and watch for incomming messages
        #self._net = wathever
        #self._net.subscribeMsg("chat,",self.onMsg)

    
    def onInput(self,e):
        msg = self._gui.getObject("Chat/ChatWindow/ChatInput").getText()
        history = self._gui.getObject("Chat/ChatWindow/ChatBox")
        history.setText("\n".join(str(history.getText()).split("\n")[:10]) + "You: " + msg)
        print msg
        #self._net.sendMsg("chat",msg)
    
    def onMsg(self,msg):
        self._gui.getControl("wathever").getText.append(msg)
    
    