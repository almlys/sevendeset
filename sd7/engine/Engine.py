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
Main Engine App (Integrates most subsystems)
"""

__version__ = "$Revision$"

__all__ = ["Engine"]


class _Engine(object):
    
    _instance = None
    _options = None
    _renderer = None
    _input = None
    _gui = None
    _hookmgr = None
    
    def __init__(self,options=None):
        _Engine._instance = self
        self.__loadDefaults(options)
        self.__loadHooks()
        self.__startRenderer()
        self.__startInput()
        self.__startGUI()
        self.__startLogic()

    def __del__(self):
        """ Stuff needs to be deleted in the correct order, if not someting
        terrible will happen """
        del self._gui
        del self._input
        del self._renderer

    def __loadDefaults(self,options):
        if options!=None:
            self._options = options
        else:
            self._options = {"global" : {} }

        # Automagically add plugins for empty config file
        if not self._options.has_key("engine.OgreRenderer.plugins"):
            self._options["engine.OgreRenderer.plugins"] = {
                        "RenderSystem_GL" : "enabled",
            }
        self._options["global"]["_engine.OgreRenderer.plugins"] = \
        self._options["engine.OgreRenderer.plugins"]


    def __startRenderer(self):
        print "** Start up the renderer **"
        from renderer.OgreRenderer import OgreRenderer as Renderer
        self._renderer = Renderer(self._options["global"])
        self._renderer.initialize()
        
    def __startInput(self):
        print "** Start up the input system **"
        from input.OISInput import OISInput as Input
        self._input = Input(self._options["global"])
        self._input.initialize()
        # Integrate it in the renderer loop (will change in iteration 2)
        self._renderer.addEventListener(self._input)
        
    def __startGUI(self):
        # Start up the GUI system
        from gui.cegui import CEGUIRenderer as GUI
        self._gui = GUI(self._options["global"],
                        "Ogre",self._renderer.getGUIGlueArgs())
        #self._gui.setController(self._hookmgr.getController("gui"))
        self._gui.initialize()
        # The GUI listens for Input events
        self._input.addEventListener(self._gui)
        self._renderer.addEventListener(self._gui)
        # CeguiOgreRenderer is already integrated into the rendering pipeline
        
    def __startPhysics(self):
        #from physics.ODEPhysics import ODEPhysics as Physics
        #self._physics = Physics(self._options["global"])
        pass
    
    def __startAudio(self):
        #from audio.OpenALAudio import OpenALAudio as Audio
        #self._audio = Audio(self._options["global"])
        pass
        
    def __startNetworking(self):
        #from networking.sd7Net import sd7Net as NetCore
        #self._netcore = NetCore(self._options["global"])
        pass
    
    def __loadHooks(self):
        from hookmgr.HookMgr import HookMgr as HookMgr
        self._hookmgr = HookMgr(self._options["global"])
        self._hookmgr.initialize()

    def __startLogic(self):
        self._hookmgr.startAutomaticControllers()
        #The Hooks (Logic) will listen to render and input events
        self._input.addEventListener(self._hookmgr)
        self._renderer.addEventListener(self._hookmgr)

    def getGUI(self):
        return self._gui


    def run(self):
        self._renderer.renderLoop()


def Engine(options=None):
    if _Engine._instance == None:
        print "Created unique instance of the engine"
        _Engine(options)
    return _Engine._instance
