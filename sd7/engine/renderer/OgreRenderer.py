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
Ogre Renderer Implementation
"""

__version__ = "$Revision$"

__all__ = ["OgreRenderer"]

import os
import os.path

import ogre.renderer.OGRE as ogre

from RendererInterface import RendererInterface

class OgreRenderer(RendererInterface):
    
    _config = None #: Configuration dict (reference to global section)
    _initialized = False #: Is the render engine initialized?
    _logDir = "log" #: Path to the log folder

    def __init__(self,options=None):
        if options!=None:
            self._config = options
        else:
            self._config = {}
        RendererInterface.__init__(self,options)

    def _setConfigDefaults(self):
        """
        Sets default config parameters
        """
        if not self._config.has_key("system.logdir"):
            self._config["system.logdir"] = "log"
        if not self._config.has_key("python.psyco"):
            self._config["python.psyco"] = "enabled"
        if not self._config.has_key("python.psyco.log"):
            self._config["python.psyco.log"] = "enabled"

        ##self.config.set("global","ogre.config","1")
        #self.config.set("global","graphics.fullscreen","0")
        #self.config.set("global","graphics.width","800")
        #self.config.set("global","graphics.height","600")
        #self.config.set("global","ogre.renderer.direct3d","1")
        #self.config.set("global","ogre.core.enabled","1")
        #self.config.set("global","ogre.core.path","data/common/OgreCore.zip")
        #self.config.set("global","data.path","data/the_forge")
        #self.config.set("global","data.common","data/common")
        #self.config.set("global","net.server","lobby01.7d7.almlys.org:7000")
        #self.config.set("global","net.bind","0.0.0.0:6000")

    def _activatePsyco(self):
        """Import Psyco if available"""
        try:
            import psyco
            psyco.full()
            if self._config["python.psyco.log"].lower() == "enabled":
                psyco.log(self._logFolder + "/psyco.log")
        except ImportError:
           pass

    def initialize(self):
        """Initialize the render engine"""
        if self._initialized:
            raise "Cannot reinit"
        self._initialized = True
        self._setConfigDefaults()
        self._logFolder = self._config["system.logdir"]
        if not os.path.exists(self._logDir):
            os.mkdir(self._logDir)
        if self._config["python.psyco"].lower() == "enabled":
            self._activatePsyco()
        if not self._setUp():
            raise "self._setUP() failed!"

    def renderLoop(self):
        """Main render loop"""
        self.initialize()
        self._root.startRendering()

    def _loadPlugins(self,plugins_path,plugins):
        print "Loading plugins..."
        for plugin in plugins:
            if plugins[plugin].lower() == "enabled":
                print "Loading Plugin %s..." %(plugin,)
                self._root.loadPlugin(plugins_path + "/" + plugin)
            else:
                print "Skipping Plugin %s..." %(plugin,)

    def _setUp(self):
        """Set up the renderer"""
        # We will manually load the plugins, and set the config
        self._root = ogre.Root("","",self._logDir + "/OgreRenderer.log")
        
        # Load Plugins
        self._loadPlugins(self._config["Engine.OgreRenderer.PluginsPath"],
        self._config["_engine.OgreRenderer.plugins"])

        # The next option avoids flickering of the framerate stats
        self._root.setFrameSmoothingPeriod (5.0)

        self._setUpResources()
        if not self._configure():
            return False
        
        self._chooseSceneManager()
        #?# self._createWorld()
        self._createCamera()
        self._createViewports()

        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        #Set Anisotropic
        ogre.MaterialManager.getSingleton().defaultAnisotropy = 8
        ogre.MaterialManager.getSingleton().setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)

        self._createResourceListener()
        self._loadResources()

        self._createScene()
        self._createFrameListener()
        return True
