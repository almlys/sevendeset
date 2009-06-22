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

import time

class _Engine(object):
    
    _instance = None
    _options = None
    _renderer = None
    _input = None
    _gui = None
    _hookmgr = None
    _worldmgr = None
    _physics = None
    _net = None
    _audio = None
    _keep_running = True
    
    def __init__(self,options=None):
        _Engine._instance = self
        try:
            self.__loadDefaults(options)
            self.__loadHooks()
            self.__startRenderer()
            self.__startInput()
            self.__startGUI()
            self.__startPhysics()
            self.__startAudio()
            self.__startNetworking()
            self.__startWorldMGR()
            self.__startLogic()
        except Exception,e:
            _Engine._instance = None
            raise e

    def __del__(self):
    #    """ Stuff needs to be deleted in the correct order, if not someting
    #    terrible will happen """
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
        self._input.addEventListener(self._gui, 0)
        self._renderer.addEventListener(self._gui)
        # CeguiOgreRenderer is already integrated into the rendering pipeline
        
    def __startPhysics(self):
        from physics.odePhysics import Physics
        self._physics = Physics(self._options["global"])
        self._physics.initialize()
    
    def __startAudio(self):
        #from audio.OpenALAudio import OpenALAudio as Audio
        #self._audio = Audio(self._options["global"])
        pass
        
    def __startNetworking(self):
        #from networking.sd7Net import sd7Net as NetCore
        #self._netcore = NetCore(self._options["global"])
        pass

    def __startWorldMGR(self):
        from renderer.ogreWorld import OgreWorld
        self._worldmgr = OgreWorld(self._options["global"])
        self._worldmgr.initialize()
    
    def __loadHooks(self):
        from hookmgr.HookMgr import HookMgr as HookMgr
        self._hookmgr = HookMgr(self._options["global"])
        self._hookmgr.initialize()

    def __startLogic(self):
        self._hookmgr.startAutomaticControllers()
        #The Hooks (Logic) will listen to render and input events
        self._input.addEventListener(self._hookmgr, 1)
        self._renderer.addEventListener(self._hookmgr)

    def __stop(self):
        def removesub(name):
            if hasattr(self,name) and getattr(self,name) is not None:
                setattr(self, name, None)
        removesub("_hookmgr")
        removesub("_physics")
        removesub("_gui")
        removesub("_input")
        removesub("_renderer")
        _Engine._instance = None

    def getGUI(self):
        return self._gui

    def getRenderer(self):
        return self._renderer

    def getHookMGR(self):
        return self._hookmgr

    def getWorldMGR(self):
        return self._worldmgr

    def getPhysics(self):
        return self._physics

    def terminate(self):
        self._keep_running = False

    def run(self):
        try:
            self.__run()
        except Exception,e:
            self.__stop()
            raise e

    def __run(self):
        #self._renderer.renderLoop()
        frmt = 1/70. # Query for monitor refresh rate!
        tst_time = time.time()
        count = 0
        ofrm = 0
        sloop_time = 0
        ssleeptime = 0
        tloop_time = 0
        tsleeptime = 0
        sleeptime = 0
        while self._keep_running:
            t0 = time.time()
            pstep = frmt
            if sleeptime < 0:
                pstep = frmt + -sleeptime
            self._physics.step(pstep)
            self._worldmgr.update()
            if not self._renderer.renderOneFrame():
                break
            loop_time = time.time()-t0
            sleeptime = frmt - loop_time
            if sleeptime <= 0:
                print "DROPING FRAMES!!!!! loop_time:%f, sl:%f" \
                    %(loop_time, sleeptime)
            self.debugMsg("%f %f %i %f" %(tloop_time,tsleeptime,ofrm,pstep))
            if sleeptime > 0:
                time.sleep(sleeptime)
            if time.time()-tst_time < 1:
                count += 1
                ssleeptime += sleeptime
                sloop_time += loop_time
            else:
                tst_time = time.time()
                ofrm = count
                tloop_time = sloop_time / count
                tsleeptime = ssleeptime / count
                sloop_time = 0
                ssleeptime = 0
                count = 0

    def debugMsg(self,msg):
        try:
            self._hookmgr.findController("Stats").writeMsg(msg)
        except:
            pass


def Engine(options=None):
    if _Engine._instance is None:
        print "Created unique instance of the engine"
        _Engine(options)
    return _Engine._instance
