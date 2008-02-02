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
Input Subsystem
"""

__version__ = "$Revision$"

__all__ = ['OISInput',]


import ogre.io.OIS as OIS

from sd7.engine.subsystem import SubSystem as SubSystem

class OISInput(SubSystem):
    
    def __init__(self,options=None):
        SubSystem.__init__(self,'OISInput',True,options)
    
    def initialize(self):
        if not SubSystem.initialize(self):
            return False
        self.log('Starting up OISInput')
        
        params = [("WINDOW",self._config['_RootWindowHandle']),
                ('XAutoRepeatOn','true')]
        
        if self._config['graphics.fullscreen'].lower() != 'true' :
            params.append(('x11_mouse_grab','false'))
            params.append(('x11_mouse_hide','false'))
            params.append(('x11_keyboard_grab','false'))
        
        self._InputManager = OIS.createPythonInputSystem(params)
        
        v = self._InputManager.getVersionNumber()
        c = 0x000000FF & v # Vendetta
        b = (0x0000FF00 & v) >> 8
        a = (0xFFFF0000 & v) >> 16
        
        self.log('OIS Version %i.%i.%i' %(a,b,c))

        #print dir(self._InputManager)
        self.log('Found %i Keyboards, %i Mouses and %i JoySticks/GamePads,etc...' \
            %(self._InputManager.numKeyBoards(),self._InputManager.numMice(),
            self._InputManager.numJoysticks()))


        self._Keyboard = self._InputManager.createInputObjectKeyboard(OIS.OISKeyboard,True)
        self._Mouse = self._InputManager.createInputObjectMouse(OIS.OISMouse,True)
        self._Joy = self._InputManager.createInputObjectJoyStick(OIS.OISJoyStick,True)
        
        return True
    
    
    def update(self):
        pass



