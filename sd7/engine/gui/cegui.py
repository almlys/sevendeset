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


class CEGUIRenderer(SubSystem):
    
    _renderer = None
    _device_type = "Ogre"
    _device = None
    _mouseWheel = 0
    
    def __init__(self,options=None,type="Ogre",args=None):
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
        self._test()
        
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

    def _test(self):
        # we will make extensive use of the WindowManager.
        wmgr = cegui.WindowManager.getSingleton()
        rootw = wmgr.createWindow("DefaultWindow", "root")
        self._guiSystem.setGUISheet(rootw)
        
        frame = wmgr.createWindow("TaharezLook/FrameWindow", "mainWindow")
        rootw.addChildWindow(frame)
        
        frame.setPosition(cegui.UVector2(cegui.UDim(0.25, 0),
            cegui.UDim(0.25, 0)))
        frame.setSize(cegui.UVector2(cegui.UDim(0.5,0), cegui.UDim(0.5,0)))
        
        frame.setText("Title sd7")
        
    def mouseMoved(self,mstate):
        #self._guiSystem.injectMouseMove(mstate.X.rel,mstate.Y.rel)
        #print mstate.X.abs,mstate.Y.abs
        self._guiSystem.injectMousePosition(mstate.X.abs,mstate.Y.abs)
        # Determine also if we moved the wheel
        if self._mouseWheel!=mstate.Z.abs:
            self._mouseWheel = mstate.Z.abs
            self._guiSystem.injectMouseWheelChange(self._mouseWheel)
            print self._mouseWheel

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

    def mouseReleased(self,mstate,id):
        self._guiSystem.injectMouseButtonUp(self._translateMouseButton(id))


