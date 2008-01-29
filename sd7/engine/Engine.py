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
        #print self._options
        from renderer import OgreRenderer as Renderer
        self._renderer = Renderer(self._options["global"])
        
    def run(self):
        self._renderer.renderLoop()

