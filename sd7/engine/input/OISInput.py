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
from sd7.engine.Events import EventType

class OISInput(SubSystem):
    
    _InputConsumers = []
    
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
        self.log('Found keyboard %s' %(self._Keyboard.vendor(),))
        self._KeyListenner = MyKeyListener(self)
        self._Keyboard.setEventCallback(self._KeyListenner)
        self.log('Translation mode is %s' %(self._Keyboard.getTextTranslation(),))

        self._Mouse = self._InputManager.createInputObjectMouse(OIS.OISMouse,True)
        self.log('Found mouse %s' %(self._Mouse.vendor(),))
        self._MouseListenner = MyMouseListener(self)
        self._Mouse.setEventCallback(self._MouseListenner)

        self._Joys = []
        self._JoyListenners = []
        id = 1
        while True:
            try:
                joy = self._InputManager.createInputObjectJoyStick(OIS.OISJoyStick,True)
                self.log('Found joy%i %s with %i buttons, %i axes, %i hats' \
                %(id,joy.vendor(),joy.buttons(),joy.axes(),joy.hats()))
                joylisten = MyJoyStickListener(id,self)
                joy.setEventCallback(joylisten)
                self._JoyListenners.append(joylisten)
                self._Joys.append(joy)
                id += 1
            except:
                break
        
        self.windowResized(self._config['graphics.width'],self._config['graphics.height'])
        
        return True
    
    def processEvent(self, ev):
        type = ev.getType()
        #if type != EventType.FRAME_STARTED and type != EventType.FRAME_ENDED:
        #    print "Got event %i" %(type,)
        if type == EventType.WIN_RESIZED:
            w, h, d, l, t = ev.getObject().getMetrics()
            self.windowResized(w,h)
        elif type == EventType.FRAME_STARTED:
            self.update()

    def windowResized(self, w, h):
        m = self._Mouse.getMouseState()
        m.width = int(w)
        m.height = int(h)
        m.X.abs = int(w) / 2
        m.Y.abs = int(h) / 2
    
    def update(self):
        self._Keyboard.capture()
        self._Mouse.capture()
        for joy in self._Joys:
            joy.capture()


class MyKeyListener(OIS.KeyListener):
    
    def __init__(self, subscriber):
        OIS.KeyListener.__init__(self)
        self._subscriber = subscriber

    def keyPressed(self, evt):
        print "Key pressed %i %s" %(evt.key,evt.text)
    
    def keyReleased(self, evt):
        print "Key released %i %s" %(evt.key,evt.text)


class MyMouseListener(OIS.MouseListener):
    
    def __init__(self, subscriber):
        OIS.MouseListener.__init__(self)
        self._subscriber = subscriber
    
    def mouseMoved(self, evt):
        print "Mouse moved"
    
    def mousePressed(self, evt, id):
        print "Mouse Pressed"
    
    def mouseReleased(self, evt, id):
        print "Mouse Released"


class MyJoyStickListener(OIS.JoyStickListener):
    
    def __init__(self, joyid, subscriber):
        OIS.JoyStickListener.__init__(self)
        self._joyid = joyid
        self._subscriber = subscriber
    
    def buttonPressed(self, evt, btn):
        print "Button pressed"
    
    def buttonReleased(self, evt, btn):
        print "Button released"
    
    def axisMoved(self, evt, axis):
        #print "Axis moved"
        pass
    
    def sliderMoved(self, evt, slider):
        print "Slider Moved"
    
    def povMoved(self, evt, pov):
        print "POV Moved"


