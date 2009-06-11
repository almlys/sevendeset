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

import random

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
        self._worldMGR.createPlane("ground",(0 ,1, 0), -10)

        self._worldMGR.createBall("ball01",(10, 100, 0), 20, 10)
        self._worldMGR.createBall("ball02",(40, 120, 0), 10, 100)
        self._worldMGR.createBall("ball03",(80, 220, 10), 25, 150)
        self._worldMGR.createBall("ball04",(120, 400, -20), 5, 12)

        for i in range(200):
            self._worldMGR.createBall("random%i" %(i),
            (-20 * random.uniform(0,0.1),i*42+150,20 * random.uniform(0,0.1)),
            15, 50)
            self._worldMGR.createBall("randoma%i" %(i),
            (-180 * random.uniform(0,0.1),i*40*random.uniform(1,5)+150,120 * random.uniform(0,0.1)),
            5, 50)
