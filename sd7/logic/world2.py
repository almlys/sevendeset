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

__all__ = ["World2"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

import random
import time

class World2(Controller):

    _balli = 0
    _last_shot = 0

    def __init__(self,params):
        Controller.__init__(self,params,"World")
        self._worldMGR = Engine().getWorldMGR()

    def initialize(self):
        Controller.initialize(self)
        self.loadScene()
        print "World was initialized"

    def terminate(self):
        self.destroyScene()

    def loadScene(self):
        self._worldMGR.setAmbientLight((0.25, 0.25, 0.25))
        #self._worldMGR.loadScene("test.xml")

        #World ground
        self._worldMGR.createPlane("ground",(0 ,1, 0), 0)

        for i in range(5):
            for j in range(5):
                self._worldMGR.createBox("box%ix%i" %(i,j), (j*20, i*25+10, 100), (20,20,20), 5)


    def destroyScene(self):
        #self._worldMGR.destroyObject("ground")
        self._worldMGR.destroyAllObjects()
        

    def onAction(self, name, down):
        if down and name == "shot" and time.time()-self._last_shot > 0.5:
            self._last_shot = time.time()
            #pos = (20, 70, 500)
            pos = Engine().getRenderer().getCamera().getRealPosition()
            ori = Engine().getRenderer().getCamera().getRealDirection()

            ball = self._worldMGR.createBall("ball%i" %(self._balli), pos, 15, 4)
            self._balli += 1
            ball.addForce(ori * 100000)




