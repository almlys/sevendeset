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

__all__ = ['World',]

from Engine import Engine
from subsystem import SubSystem

class World(SubSystem):

    def __init__(self, options):
        SubSystem.__init__(self,"WorldManager", True, options)
        self._sceneManager = Engine().getRenderer().getSceneManager()

    def loadScene(self,name):
        print name

    def loadObject(self,name):
        pass

    def setAmbientLight(self,a):
        self._sceneManager.setAmbientLight(a)

    def createPlane(self,vnormal,konstant):

        plane = ogre.Plane((0, 1, 0), 0)
        #self.floor = ode.GeomPlane(self.space, (0,1,0), 0.0)

        mm = ogre.MeshManager.getSingleton()
        mm.createPlane('ground', ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME,
                       plane, 1500, 1500, 20, 20, True, 1, 5, 5, (0, 0, 1))

        ent = self._sceneManager.createEntity("GroundEntity", "ground")
        try:
            self._sceneManager.rootSceneNode.createChildSceneNode().attachObject(ent)
        except AttributeError:
            self._sceneManager.getRootSceneNode().createChildSceneNode().attachObject(ent)
        ent.setMaterialName("Material.002/SOLID")

