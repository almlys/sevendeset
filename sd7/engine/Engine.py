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


class Engine(object):
    
    _options = None
    
    def __init__(self,options=None):
        if options!=None:
            self._options = options
        else:
            self._options = {"global" : {} }
            
        print "** Find plugin list **"
        if self._options.has_key("engine.OgreRenderer.plugins"):
            self._options["global"]["_engine.OgreRenderer.plugins"] = \
            self._options["engine.OgreRenderer.plugins"]
        #else:
        #    self._options["engine.OgreRenderer.plugins"] = {
        #                "RenderSystem_GL" : "enabled",
        #    }
        
        print "** Start up the renderer **"
        from renderer.OgreRenderer import OgreRenderer as Renderer
        print "->new"
        self._renderer = Renderer(self._options["global"])
        print "->init"
        self._renderer.initialize()
        
        print "** Start up the input system **"
        from input.OISInput import OISInput as Input
        self._input = Input(self._options["global"])
        self._input.initialize()
        # Integrate it in the renderer loop (will change in iteration 2)
        self._renderer.addEventListener(self._input)
        
        # Start up the GUI system
        from gui.cegui import CEGUIRenderer as GUI
        self._gui = GUI(self._options["global"],
                        "Ogre",self._renderer.getGUIGlueArgs())
        self._gui.initialize()
        # The GUI listens for Input events
        self._input.addEventListener(self._gui)
        # CeguiOgreRenderer is already integrated into the rendering pipeline
        
        
        #from physics.ODEPhysics import ODEPhysics as Physics
        #self._physics = Physics(self._options["global"])
        #from audio.OpenALAudio import OpenALAudio as Audio
        #self._audio = Audio(self._options["global"])
        #from networking.sd7Net import sd7Net as NetCore
        #self._netcore = NetCore(self._options["global"])

    def __del__(self):
        """ Stuff needs to be deleted in the correct order, if not someting
        terrible will happen """
        del self._gui
        del self._input
        del self._renderer

    def run(self):
        self._renderer.renderLoop()

