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

__all__ = ["CEGUIRenderer"]


import ogre.gui.CEGUI as cegui

from sd7.engine.subsystem import SubSystem as SubSystem
from sd7.engine.Events import EventType

class CEGUIRenderer(SubSystem):
    
    _renderer = None
    _device_type = "Ogre"
    _device = None
    _mouseWheel = 0
    _eventSubscribers = {}
    _guiFocus = False
    _mouseEnabled = False
    _keyboardEnabled = False
    
    def __init__(self,options=None,type="Ogre",args=None):
        """
        @param options: Set of options to configure the GUI
        @param type: String with the type of renderer, Ogre is the only currently one allowed
        @param args: Specific arguments of the renderer, required to glue both systems
        """
        SubSystem.__init__(self,'CEGUIRenderer',True,options)
        self._device_type = type
        self._device_args = args

    def __del__(self):
        self.log("Destroying GUI")
        # This delete if important, if you ommit it, then you will have a nice
        # KABOUUM!!
        del self._guiSystem
        del self._renderer

    def initialize(self):
        """ Initialization """
        
        if not SubSystem.initialize(self):
            return False
        self.log('Starting up CEGUI')
        
        if not self._initCEGUI():
            return False
        
        self._loadResources()
        self._createRootWindow()
        #self._test()
        
        return True

    def _initCEGUI(self):
        """ Inits CEGUI """
        
        # CEGUI can only be attached to (used with) a:
        # * DiretX device
        # * OpenGL Renderer
        # * Ogre Render Window <- Currently being used
        # * Irrlicht Renderer
        #renderWindow,  sceneManager = self._device_args
        #self._renderer = cegui.OgreCEGUIRenderer(renderWindow._getOgreRenderWindow(),
        #    ogre.RENDER_QUEUE_OVERLAY, False, 0, sceneManager._getOgreSceneManager())
        self._renderer = cegui.OgreCEGUIRenderer(*self._device_args)
        self._guiSystem = cegui.System(self._renderer,None,None,None,
            "",self._logDir + "/CEGUI.log")
        
        # Remember the OgreCEGUIRenderer already updates the gui on its render loop
        # for other devices you need to manually update the gui "renderGUI()"
        
        logger = cegui.Logger.getSingleton()
        #logger.setLoggingLevel(cegui.Informative)
        logger.setLoggingLevel(cegui.Insane)
        
        return True
    
        
    def _loadResources(self):
        # load scheme and set up defaults
        cegui.SchemeManager.getSingleton().loadScheme("TaharezLook.scheme")
        self._guiSystem.setDefaultMouseCursor("TaharezLook",  "MouseArrow")
        cegui.FontManager.getSingleton().createFont("Commonwealth-10.font")

    def _createRootWindow(self):
        self._wmgr = cegui.WindowManager.getSingleton()
        self._rootw = self._wmgr.createWindow("DefaultWindow", "root")
        self._guiSystem.setGUISheet(self._rootw)


    def _test(self):
        frame = self._wmgr.createWindow("TaharezLook/FrameWindow", "mainWindow")
        self._rootw.addChildWindow(frame)
        
        frame.setPosition(cegui.UVector2(cegui.UDim(0.25, 0),
            cegui.UDim(0.25, 0)))
        frame.setSize(cegui.UVector2(cegui.UDim(0.5,0), cegui.UDim(0.5,0)))
        
        frame.setText("Title sd7")

    ### Client functions

    def loadView(self,name,parent="root"):
        """ Loads a set of Windows conforming a view
            @param name: The name of the file containing the layout definition
            @param parent: The name of the parent window
        """
        self.log("Loading layout %s" %(name,))
        guiLayout = self._wmgr.loadWindowLayout(name)
        self._wmgr.getWindow(parent).addChildWindow(guiLayout)
        #self._rootw.addChildWindow(guiLayout)
    

    def destroyObject(self,name):
        return self._wmgr.destroyWindow(name)

    def getObject(self,name):
        return self._wmgr.getWindow(name)
    
    def subscribeEvent(self,ctrl_name,event,func):
        """
        Bind and event to a function
        @param ctrl_name: The name of the window/control to watch for events
        """
        wctrl = self._wmgr.getWindow(ctrl_name)
        #self._addEvent(ctrl_name,event,func)
        #wctrl.subscribeEvent(event, self, "_processEvents")
        # Se podria hacer con un Proxy
        wctrl.subscribeEvent(self.getEvent(event), func.im_self, func.__name__)


    def getEvent(self,str):
        """
        Returns the selected event name
        @param str: Name of the event to find
        """
        klass, event = str.split("/")
        return getattr(getattr(cegui,klass),event)

    def toggleFocus(self, focus = None):
        """
        Toggles the GUI focus state
        @param focus: True or False to force the focus state
        """
        if focus is None:
            self._guiFocus = not self._guiFocus
        else:
            self._guiFocus = focus

    def toggleMouse(self, enabled = None):
        """
        Enables/Disables the Mouse
        """
        if enabled is None:
            self._mouseEnabled = not self._mouseEnabled
        else:
            self._mouseEnabled = enabled
        #print dir(cegui.MouseCursor)
        cegui.MouseCursor.getSingleton().setVisible(self._mouseEnabled)

    def toggleKeyboard(self, enabled = None):
        """
        Enables/Disables the Keyboard
        """
        if enabled is None:
            self._keyboardEnabled = not self._keyboardEnabled
        else:
            self._keyboardEnabled = enabled

    def hasFocus(self):
        return self._guiFocus

    # End client methods

    def processEvent(self, ev):
        if not self.hasFocus():
            return False
        type = ev.getType()
        if type == EventType.KEY_PRESSED:
            return self.keyPressed(ev.getObject())
        elif type == EventType.KEY_RELEASED:
            return self.keyReleased(ev.getObject())
        elif type == EventType.MOUSE_MOVED:
            return self.mouseMoved(ev.getObject())
        elif type == EventType.MOUSE_PRESSED:
            return self.mousePressed(ev.getObject(), ev.getObject().id)
        elif type == EventType.MOUSE_RELEASED:
            return self.mouseReleased(ev.getObject(), ev.getObject().id)
        return False

    def mouseMoved(self,mstate):
        #self._guiSystem.injectMouseMove(mstate.X.rel,mstate.Y.rel)
        #print mstate.X.abs,mstate.Y.abs
        self._guiSystem.injectMousePosition(mstate.X.abs,mstate.Y.abs)
        # Determine also if we moved the wheel
        if self._mouseWheel!=mstate.Z.abs:
            self._mouseWheel = mstate.Z.abs
            self._guiSystem.injectMouseWheelChange(self._mouseWheel)
            #print self._mouseWheel
        return True
            

    def _translateMouseButton(self,id):
        if id ==0:
            return cegui.LeftButton
        elif id ==1:
            return cegui.RightButton
        elif id ==2:
            return cegui.MiddleButton
        elif id ==3:
            return cegui.X1Button
        elif id ==4:
            return cegui.X2Button
        else:
            return cegui.LeftButton

    def mousePressed(self,mstate,id):
        self._guiSystem.injectMouseButtonDown(self._translateMouseButton(id))
        return True

    def mouseReleased(self,mstate,id):
        self._guiSystem.injectMouseButtonUp(self._translateMouseButton(id))
        return True

    def keyPressed(self,ev):
        #print ev.key
        self._guiSystem.injectKeyDown(ev.key)
        self._guiSystem.injectChar(ev.text)
        return True

    def keyReleased(self,ev):
        self._guiSystem.injectKeyUp(ev.key)
        return True
        


