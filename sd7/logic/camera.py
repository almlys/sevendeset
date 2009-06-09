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

__all__ = ["Camera"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

class Camera(Controller):

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


    def initialize(self):
        Controller.initialize(self)
        self.log("Initializing %s" %(self.__class__.__name__))

    def onFrame(self,evt):
        time = evt.getObject().timeSinceLastFrame
        
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
        

    