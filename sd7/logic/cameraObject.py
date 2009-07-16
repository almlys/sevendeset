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

__all__ = ["CameraObject"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class CameraObject(Controller):

    _mouse = False
    _rotateX = 0
    _rotateY = 0
    _moveZ = 0
    _moveX = 0
    _movementMap = {
        "rotate_up" : { True : 1, False : 0},
        "rotate_down" : { True : -1, False : 0},
        "rotate_left" : { True : 1, False : 0},
        "rotate_right" : { True : -1, False : 0},
        "up" : { True : -1, False : 0},
        "down" : { True : 1, False : 0},
        "right" : { True : 1, False : 0},
        "left" : { True : -1, False : 0},
    }

    
    def __init__(self,params):
        Controller.__init__(self,params)
        self._renderer = Engine().getRenderer()
        self._camera = self._renderer.getCamera()
        self._updateMetrics()
        self._target = None

    def _updateMetrics(self):
        w, h, c, l, t = self._renderer.getRenderWindow().getMetrics()
        wd = w/3
        hd = h/3
        self._frontier = [wd, 2*wd, hd, 2*hd]

    def initialize(self):
        Controller.initialize(self)
        self.log("Initializing %s" %(self.__class__.__name__))

    def setTarget(self, name):
        self._targetName = name
        self._target = Engine().getWorldMGR().findObject("tank_%s" %(name,));

    def onFrame(self,evt):
        time = evt.timeSinceLastFrame
        
        if time == 0:
            rotateScaleX = 0.1 * self._rotateX
            rotateScaleY = 0.1 * self._rotateY
            moveScaleZ = 1 * self._moveZ
            moveScaleX = 1 * self._moveX
        else:
            rotateScaleX = 2 * time * self._rotateX
            rotateScaleY = 2 * time * self._rotateY
            moveScaleZ = 100 * time * self._moveZ
            moveScaleX = 70 * time * self._moveX

        if rotateScaleX != 0:
            self._camera.pitch(rotateScaleX)
        if rotateScaleY != 0:
            self._camera.yaw(rotateScaleY)

        if moveScaleZ != 0 or moveScaleX != 0:
            #vector = self._renderer.getRendererFactory().createVector3()
            self._camera.moveRelative((moveScaleX,0,moveScaleZ))

        if self._target != None and moveScaleZ != 0:
            self._target.addForce((0, 0 , moveScaleZ * 2000))


        #self._mouse += time

        #if self._mouse >= 0.2:
        #    self._rotateX = 0
        #    self._rotateY = 0
        #    self._mouse = False


    def onAction(self, name, down):
        if name in ("rotate_up", "rotate_down"):
            self._rotateX = self._movementMap[name][down]
            return True
        elif name in ("rotate_left", "rotate_right"):
            self._rotateY = self._movementMap[name][down]
            return True
        elif name in ("up", "down"):
            self._moveZ = self._movementMap[name][down]
            return True
        elif name in ("right", "left"):
            self._moveX = self._movementMap[name][down]
            return True
        return False

    def onAxis(self, name, abs, rel, type):
        return False
        #self._mouse = 0
        x1, x2, y1, y2 = self._frontier
        neg = 1
        if abs < 0:
            neg = -1
        abs = neg * abs
        speed = 0.0013

        if name == "x":
            if abs < x1:
                self._rotateY = (x1 - abs) * speed * neg
            elif abs > x2:
                self._rotateY = (abs - x2) * speed * -neg
            else:
                self._rotateY = 0
            return True
        if name == "y":
            if abs < x1:
                self._rotateX = (y1 - abs) * speed * neg
            elif abs > x2:
                self._rotateX = (abs - y2) * speed * -neg
            else:
                self._rotateX = 0
            return True
        return False
            


    