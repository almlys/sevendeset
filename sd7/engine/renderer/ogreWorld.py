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

__all__ = ['OgreWorld',]

from sd7.engine.Engine import Engine
from sd7.engine.subsystem import SubSystem

import ogre.renderer.OGRE as ogre

class SceneObject(object):

    def __init__(self, name, node, phys):
        self.name = name
        self.physical = phys
        self.node = node
    

class OgreWorld(SubSystem):

    def __init__(self, options):
        SubSystem.__init__(self,"WorldManager", True, options)
        self._sceneManager = Engine().getRenderer().getSceneManager()._getOgreSceneManager()
        self._simulator = Engine().getPhysics()
        self._staticObjects = {}
        self._dynaObjects = {}

    def loadScene(self,name):
        print name

    def loadObject(self,name):
        pass

    def setAmbientLight(self,a):
        #self._sceneManager.setAmbientLight(a)
        self._sceneManager.ambientLight = a

    def createPlane(self, name, normal = (0,1,0), cons = 0.0):

        physical = self._simulator.createGeomPlane(normal, cons)

        # View
        plane = ogre.Plane( normal, cons)

        mm = ogre.MeshManager.getSingleton()
        mm.createPlane(name, ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME,
                       plane, 55500, 55500, 20, 20, True, 1, 5, 5, (0, 0, 1))

        ent = self._sceneManager.createEntity(name, name)
        node = self._sceneManager.getRootSceneNode().createChildSceneNode()
        node.attachObject(ent)
        ent.setMaterialName("Material.002/SOLID")

        self._staticObjects[name] = SceneObject(name, node, physical)

    def createBall(self, name, position=(10, 100, 0), scale = 20.0, mass = 50):
        # Draw ball
        ent = self._sceneManager.createEntity(name, "Sphere.mesh")
        node = self._sceneManager.getRootSceneNode().createChildSceneNode()
        node.attachObject(ent)
        node.setScale((scale, scale, scale))
        node.setPosition(position)

        # Physics ball
        body = self._simulator.newBody()
        M = self._simulator.newMass()
        M.setSphere(500, scale)
        M.mass = mass
        body.setMass(M)
        body.setPosition(position)
        geom = self._simulator.createGeomSphere(scale)
        geom.setBody(body)

        self._dynaObjects[name] = SceneObject(name, node, geom)

        #ent = sceneManager.createEntity("Ninja", "ninja.mesh")
        #node = sceneManager.rootSceneNode.createChildSceneNode("NinjaNode")
        #node.attachObject(ent)

    def update(self):
        for a in self._dynaObjects.keys():
            obj = self._dynaObjects[a]
            obj.node.setPosition(obj.physical.getPosition())
            obj.node.setOrientation(obj.physical.getQuaternion())
            #print obj.physical.getRotation()

