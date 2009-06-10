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

__all__ = ["Stats"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class Stats(Controller):

    def __init__(self,params):
        Controller.__init__(self,params,"stats")
        self._msg2 = ""
        self._msg1 = ""
        self._markee = "sd7 Engine - Demostration"
        self._i = 0
        self._time = 0

    def initialize(self):
        Controller.initialize(self)

        # get the GUI and load the chat View
        self._gui = Engine().getGUI()
        self._gui.loadView("stats.layout")
        # Watch for input events
        #self._gui.subscribeEvent("Chat/ChatWindow/ChatOkBtn",
        #    self._gui.getEvent("PushButton/EventClicked"),self.onInput)
        self._textObject = self._gui.getObject("StatsWindow/Msg")
        self._winstats = self._gui.getObject("StatsWindow")
        self.setText("...")
        self._window = Engine().getRenderer().getRenderWindow()
        
        if self._params.has_key("visible") \
            and self._params["visible"].lower() != "true":
            self._vis = False
        else:
            self._vis = True
        self._winstats.setVisible(self._vis)

    def terminate(self):
        self._gui.destroyObject("StatsWindow")
        Controller.terminate(self)

    def writeMsg(self,msg):
        self._msg1 = msg


    def setText(self,msg):
        self._textObject.setText(msg)

    def onAction(self, name, down):
        if down and name == "stats":
            self._vis = not self._vis
            self._winstats.setVisible(self._vis)
            return True


    def onFrame(self, evt):
        time = evt.timeSinceLastFrame

        # Do stupid things..
        self._time += time
        if self._i <= len(self._markee) and self._time > 0.123:
            self._msg2 = self._markee[0:self._i]
            self._i += 1
            self._time = 0
            #print self._msg2
        elif self._time > 1.5:
            self._i = 0
            self._msg2 = ""
            self._time = -0.434


        s = self._window.getStatistics()
        self.setText("FPS %.2f (%.2f) B/W:%.2f/%.2f t,b : %i , %i\n%s\n%s"\
            %(s.avgFPS, s.lastFPS,
            s.bestFrameTime, s.worstFrameTime, s.triangleCount,
            s.batchCount, self._msg1, self._msg2))




