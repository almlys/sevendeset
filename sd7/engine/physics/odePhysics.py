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

__all__ = ['Physics',]

import ode

from sd7.engine.subsystem import SubSystem


class Physics(SubSystem):

    def __init__(self, options = None):
        SubSystem.__init__(self, "ODEPhysics", True, options)

    def initialize(self):
        if not SubSystem.initialize(self):
            return False
        # Crating ode world
        self._world = ode.World()
        self._world.setGravity( (0, -9.81, 0))
        self._space = ode.Space()
        self._contactGroup = ode.JointGroup()
        

    def _collision(self, args, geom1, geom2):
        # Check if the objects do collide
        contacts = ode.collide(geom1, geom2)

        # Create contact joints
        world,contactgroup = args
        for c in contacts:
            c.setBounce(0.2)
            c.setMu(5000)
            j = ode.ContactJoint(world, contactgroup, c)
            j.attach(geom1.getBody(), geom2.getBody())
        

    def step(self, dt):
        self._space.collide((self._world, self._contactGroup), self._collision)
        self._world.step(dt)
        self._contactGroup.empty()

    def newBody(self):
        return ode.Body(self._world)

    def newMass(self):
        return ode.Mass()


    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError, e:
            if name.startswith("create"):
                self.__createName = name[6:]
                return self.__create
            raise e

    def __create(self,*args):
        return getattr(ode,self.__createName)(self._space, *args)

    def destroyGeom(self, geom):
        self._space.remove(geom)
