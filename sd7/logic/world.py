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

__all__ = ["World"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class World(Controller):

    def __init__(self,params):
        Controller.__init__(self,params,"World")
        self._worldMGR = Engine().getWorldMGR()

    def initialize(self):
        Controller.initialize(self)
        self.loadScene()
        print "World was initialized"

    def loadScene(self):
        self._worldMGR.setAmbientLight((0.25, 0.25, 0.25))
        #self._worldMGR.loadScene("test.xml")

        #World ground
        self._worldMGR.createPlane((0 ,1, 0), 0)


