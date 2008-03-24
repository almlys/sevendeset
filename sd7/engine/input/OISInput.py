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
    """ OIS Input subsytem """
    
    _InputConsumers = []
    
    def __init__(self,options=None):
        SubSystem.__init__(self,'OISInput',True,options)
    
    def initialize(self):
        """ Initialization """
        
        if not SubSystem.initialize(self):
            return False
        self.log('Starting up OISInput')
        
        if not self._initializeOIS():
            return False
        
        return True
    
    def _initializeOIS(self):
        """ Creates the root OIS InputManager """
        # Window handle
        params = [("WINDOW",self._config['_RootWindowHandle']),
                ('XAutoRepeatOn','true')]
        
        # mouse grab/hide only on fullscreen mode
        # Notice the current code is platform dependent!!!
        # It will do nothing on non-linux systems since the options have
        # other names, I think that upstream (OIS maintainers), should have
        # used a set of generic options mapped to the corresponding OS attrs
        if self._config['graphics.fullscreen'].lower() != 'true' :
            params.append(('x11_mouse_grab','false'))
            params.append(('x11_mouse_hide','false'))
            params.append(('x11_keyboard_grab','false'))
        
        self._InputManager = OIS.createPythonInputSystem(params)
        
        self._printOISVersion()
        return self._initalizeAndRegisterListenners()
    
    def _printOISVersion(self):
        """ Prints to the logs which version of OIS are we using """
        v = self._InputManager.getVersionNumber()
        c = 0x000000FF & v # Vendetta
        b = (0x0000FF00 & v) >> 8
        a = (0xFFFF0000 & v) >> 16
        
        self.log('OIS Version %i.%i.%i' %(a,b,c))

    def _initalizeAndRegisterListenners(self):
        """ Initializes all the avaliable InputDevices, and associates them to
        the corresponding listenners """
        self.log('Found %i Keyboards, %i Mouses and %i JoySticks/GamePads,etc...' \
            %(self._InputManager.getNumberOfDevices(OIS.Type.OISKeyboard),
            self._InputManager.getNumberOfDevices(OIS.Type.OISMouse),
            self._InputManager.getNumberOfDevices(OIS.Type.OISJoyStick)))


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
        """ Update the Mouse area size, according to the new window size """
        m = self._Mouse.getMouseState()
        m.width = int(w)
        m.height = int(h)
        m.X.abs = int(w) / 2
        m.Y.abs = int(h) / 2
    
    def update(self):
        """ Update all devices (this any callbacks for any input event) """
        self._Keyboard.capture()
        self._Mouse.capture()
        for joy in self._Joys:
            joy.capture()


class MyKeyListener(OIS.KeyListener):
    """ Keyboard Key Listenner, there can be only be ONE, if you want to
    controll aditional keyboards attached to the systems then OIS is not
     he suitable API, altough you first will need to fight with your OS"""
    
    def __init__(self, subscriber):
        OIS.KeyListener.__init__(self)
        self._subscriber = subscriber

    def keyPressed(self, evt):
        print "Key pressed %i %s" %(evt.key,evt.text)
    
    def keyReleased(self, evt):
        print "Key released %i %s" %(evt.key,evt.text)


class MyMouseListener(OIS.MouseListener):
    """ Mouse Listenner, there can be only ONE, if you want to control
    more read MyKeyListener docstring """
    
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
    """ Our OS may have, more than one Joystick, gamepad, etc.. device"""
    
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


