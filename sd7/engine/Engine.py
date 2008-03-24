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
            
        # Find plugin list
        if self._options.has_key("engine.OgreRenderer.plugins"):
            self._options["global"]["_engine.OgreRenderer.plugins"] = \
            self._options["engine.OgreRenderer.plugins"]
        #else:
        #    self._options["engine.OgreRenderer.plugins"] = {
        #                "RenderSystem_GL" : "enabled",
        #    }
        
        # Start up the renderer
        from renderer.OgreRenderer import OgreRenderer as Renderer
        self._renderer = Renderer(self._options["global"])
        self._renderer.initialize()
        
        # Start up the input system
        from input.OISInput import OISInput as Input
        self._input = Input(self._options["global"])
        self._input.initialize()
        # Integrate it in the renderer loop (will change in iteration 2)
        self._renderer.addEventListener(self._input)
        
        
        #from physics.ODEPhysics import ODEPhysics as Physics
        #self._physics = Physics(self._options["global"])
        #from audio.OpenALAudio import OpenALAudio as Audio
        #self._audio = Audio(self._options["global"])
        #from networking.sd7Net import sd7Net as NetCore
        #self._netcore = NetCore(self._options["global"])
        

    def run(self):
        self._renderer.renderLoop()

