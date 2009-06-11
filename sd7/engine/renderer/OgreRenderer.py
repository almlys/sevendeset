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


from sd7.engine.subsystem import SubSystem as SubSystem
from sd7.engine.Events import Event, EventType
from RendererInterface import RendererInterface

class RendererFactory(object):

    def __init__(self):
        pass

    def createVector3(self,x,y,z):
        return ogre.Vector3(x,y,z)



class OgreRenderer(SubSystem,RendererInterface):
    
    _renderWindow = None #: The render window
    _sceneManager = None
    _subscribers = [] #: Event subscribers

    def __init__(self,options=None):
        SubSystem.__init__(self,'OgreRenderer',True,options)
        RendererInterface.__init__(self,options)
        self._rendererFactory = RendererFactory()

    def __del__(self):
        self.log("Destroying Renderer")
        #del self._renderWindow
        #del self._sceneManager

    def _setConfigDefaults(self):
        """
        Sets default config parameters
        """
        SubSystem._setConfigDefaults(self)
        if not self._config.has_key("python.psyco"):
            self._config["python.psyco"] = "enabled"
        if not self._config.has_key("python.psyco.log"):
            self._config["python.psyco.log"] = "enabled"
        if not self._config.has_key("ogre.renderer"):
            self._config["ogre.renderer"] = "OpenGL"
        if not self._config.has_key("graphics.fullscreen"):
            self._config["graphics.fullscreen"] = "false"
        if not self._config.has_key("graphics.width"):
            self._config["graphics.width"] = "800"
        if not self._config.has_key("graphics.height"):
            self._config["graphics.height"] = "600"
        if not self._config.has_key("_window.name"):
            self._config["_window.name"] = "7d7 Engine"

        ##self.config.set("global","ogre.config","1")
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
                psyco.log(self._logDir + "/psyco.log")
        except ImportError:
           pass

    def initialize(self):
        if not SubSystem.initialize(self):
            return False
        if self._config["python.psyco"].lower() == "enabled":
            self._activatePsyco()
        a,b,c,d = ogre.GetOgreVersion()
        print "Using Ogre %s.%s.%s %s" %(a,b,c,d)
        a,b,c = ogre.GetPythonOgreVersion()
        print "Using Python-Ogre %s.%s.%s" %(a,b,c)
        if not self._setUp():
            raise "self._setUP() failed!"
        return True
    
    def renderLoop(self):
        """Main render loop"""
        #self.initialize()
        self._root.startRendering()

    def renderOneFrame(self):
        ogre.WindowEventUtilities.messagePump()
        return self._root.renderOneFrame()

    def _loadPlugins(self,plugins_path,plugins):
        self.log("Loading plugins...")
        for plugin in plugins:
            if plugins[plugin].lower() == "enabled":
                self.log("Loading Plugin %s..." %(plugin,))
                self._root.loadPlugin(plugins_path + "/" + plugin)
            else:
                self.log("Skipping Plugin %s..." %(plugin,))

    def _setUpResources(self):
        """Set up initial BootStrap resources"""
        #ogre.ResourceGroupManager.getSingleton().\
        #addResourceLocation("data/system/OgreCore.zip", "Zip", "Bootstrap")
        ogre.ResourceGroupManager.getSingleton().\
        addResourceLocation("data/system/common", "FileSystem", "General",True)


    def _configure(self):
        """Create the render window depending of the configured settings"""
        found = False
        renList = self._root.getAvailableRenderers()
        
        self.log("Available render subsystems: ")
        for r in renList:
            self.log(r.getName())
            if r.getName().startswith(self._config["ogre.renderer"]):
                self._root.setRenderSystem(r)
                found = True
                self.log("%s found and set" %(r.getName(),))

        if not found:
            self.log("No Renderer was found in your system!")
            return False
        else:
            self.log("root.initialize")
            self._root.initialise(False)
            self.log("checking window properties...")
            fullScreen = self._config["graphics.fullscreen"].lower() == "true"
            w=int(self._config["graphics.width"])
            h=int(self._config["graphics.height"])

            self.log("Creating window... %sx%s fullscreen:%i" %(w,h,fullScreen))
            # Throws OGREException if VideoCard is not found (cannot create GLXContext)
            self._renderWindow = self._root.createRenderWindow(
                self._config["_window.name"], w, h, fullScreen)
            self.log("saving window handle")
            #print dir(self._renderWindow)
            #print self._renderWindow.getCustomAttributeInt
            #help(self._renderWindow.getCustomAttributeInt)
            print "Window HANDLE: %i" %(self._renderWindow.getCustomAttributeUnsignedLong("WINDOW"),)
            self._config["_RootWindowHandle"] = \
                str(self._renderWindow.getCustomAttributeUnsignedLong("WINDOW"))
                # 64 bits, guy, it's a long, if not KAAAAAAABOOOOOOOOOUMMMMMMMMMMMMMMM!!!
            self.log("Window created..")
            return True

    def _chooseSceneManager(self):
        """Chooses a default SceneManager."""
        self._sceneManager = self._root.createSceneManager(ogre.ST_GENERIC,"MainSceneManager")

    def _createCamera(self):
        """Creates the camera."""        
        self._camera = self._sceneManager.createCamera('PlayerCam')
        self._camera.setPosition(0, 0, 500)
        self._camera.lookAt((0, 0, -300))
        self._camera.setNearClipDistance(5)

    def _createViewports(self):
        """Creates the Viewport."""
        self._viewport = self._renderWindow.addViewport(self._camera)
        self._viewport.backgroundColour = (0,0,0)

    def _loadResources(self):
        """This loads all initial resources.  Redefine this if you do not want
        to load all resources at startup."""
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()

    def _createFrameListener(self):
        """Creates the FrameListener."""
        self._frameListener = EventListener(self._renderWindow, self._subscribers)
        self._root.addFrameListener(self._frameListener)
        ogre.WindowEventUtilities.addWindowEventListener(self._renderWindow, self._frameListener)

    def _setUpLogging(self):
        global _logMgr #very dirty workarround until I patch ogre (deleting _logMgr = KaBoum)
        _logMgr = ogre.LogManager()
        #logMgr = ogre.LogManager.getSingletonPtr()
        self._ogreLog = _logMgr.createLog(self._logDir + '/Ogre.log',True,False,False)
        
#        class MyLog(ogre.LogListener):
#            
#            def messageLogged(self, message, level, debug, logName):
#                self.logFile(message)
#        

    def _setUp(self):
        """Set up the renderer"""
        self._setUpLogging()
        
        # We will manually load the plugins, and set the config
        self._root = ogre.Root("","","")
        
        # Load Plugins
        self.log("Loading plugins")
        self._loadPlugins(self._config["Engine.OgreRenderer.PluginsPath"],
        self._config["_engine.OgreRenderer.plugins"])

        # The next option avoids flickering of the framerate stats
        self._root.setFrameSmoothingPeriod(5.0)

        self.log("Setting up resources...")
        self._setUpResources()
        self.log("Configuring...")
        # Load configuration
        if not self._configure():
            return False
        
        self.log("Choosing scene Manager...")
        self._chooseSceneManager()
        #self._createWorld()
        self._createCamera()
        self._createViewports()

        #STOP HERE! - TODO - Query For hardware capabilities and set the values
        # according to them.
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        #Set Anisotropic
        ogre.MaterialManager.getSingleton().setDefaultAnisotropy(8)
        ogre.MaterialManager.getSingleton().setDefaultTextureFiltering(ogre.TFO_ANISOTROPIC)

        #self._createResourceListener()
        self._loadResources()

        self._createScene()
        self._createFrameListener()
        return True
    
    def _createScene(self):
        self._sceneManager.ambientLight = 0.25, 0.25, 0.25

        #World ground
        plane = ogre.Plane((0, 1, 0), 0)
        #self.floor = ode.GeomPlane(self.space, (0,1,0), 0.0)

        mm = ogre.MeshManager.getSingleton()
        mm.createPlane('ground', ogre.ResourceGroupManager.DEFAULT_RESOURCE_GROUP_NAME,
                       plane, 1500, 1500, 20, 20, True, 1, 5, 5, (0, 0, 1))

        ent = self._sceneManager.createEntity("GroundEntity", "ground")
        try:
            self._sceneManager.rootSceneNode.createChildSceneNode().attachObject(ent)
        except AttributeError:
            self._sceneManager.getRootSceneNode().createChildSceneNode().attachObject(ent)
        ent.setMaterialName("Material.002/SOLID")

        # Ogre ball 1
        ent1 = self._sceneManager.createEntity("ball1", "Sphere.mesh")
        try:
            node1 = self._sceneManager.rootSceneNode.createChildSceneNode()
        except AttributeError:
            node1 = self._sceneManager.getRootSceneNode().createChildSceneNode()
        node1.attachObject(ent1)
        node1.scale = ((1.8, 1.8, 1.8))

        # ODE ball 1
        #body1 = ode.Body(self.world)
        #M = ode.Mass()
        #M.setSphere(500, 0.05)
        #M.mass = 50
        #body1.setMass(M)
        #body1.setPosition((10, 100, 0))
        #geom = ode.GeomSphere(self.space, 50.0)
        #geom.setBody(body1)

        # Add ball 1 to the body list
        #self.bodyList.append((body1, node1))

        #ent = sceneManager.createEntity("Ninja", "ninja.mesh")
        #node = sceneManager.rootSceneNode.createChildSceneNode("NinjaNode")
        #node.attachObject(ent)

        ent = self._sceneManager.createEntity("Cube", "Cube.mesh")
        try:
            node = self._sceneManager.rootSceneNode.createChildSceneNode("CubeNode")
        except AttributeError:
            node = self._sceneManager.getRootSceneNode().createChildSceneNode("CubeNode")
        node.attachObject(ent)
        node.translate(0,10,0)

        #body1 = ode.Body(self.world)
        #M = ode.Mass()
        #M.mass = 30
        #M.setSphere(500, 0.05)
        #body1.setMass(M)
        #body1.setPosition((11, 500, 0))
        #geom = ode.GeomSphere(self.space, 5.0)
        #geom.setBody(body1)
        #self.bodyList.append((body1, node))


        ent2 = self._sceneManager.createEntity("Circle", "Cube.001.mesh")
        try:
            node2 = self._sceneManager.rootSceneNode.createChildSceneNode("CircleNode")
        except AttributeError:
            node2 = self._sceneManager.getRootSceneNode().createChildSceneNode("CircleNode")
        node2.attachObject(ent2)

        #body1 = ode.Body(self.world)
        #M = ode.Mass()
        #M.setSphere(500, 0.05)
        #M.mass = 10.5
        #body1.setMass(M)
        #body1.setPosition((9, 550, 0))
        #geom = ode.GeomSphere(self.space, 5.0)
        #geom.setBody(body1)
        #self.bodyList.append((body1, node2))


        light = self._sceneManager.createLight("Light1")
        light.type = ogre.Light.LT_POINT
        light.position = 250, 150, 250
        light.diffuseColour = 1, 1, 1
        light.specularColour = 1, 1, 1

        # create the first camera node/pitch node
        try:
            node = self._sceneManager.rootSceneNode.createChildSceneNode("CamNode1", (-400, 200, 400))
        except AttributeError:
            node = self._sceneManager.getRootSceneNode().createChildSceneNode("CamNode1", (-400, 200, 400))
        node.yaw(ogre.Degree(-45))  # look at the ninja

        node = node.createChildSceneNode("PitchNode1")
        node.attachObject(self._camera)

        # create the second camera node/pitch node
        try:
            node = self._sceneManager.rootSceneNode.createChildSceneNode("CamNode2", (0, 200, 400))
        except AttributeError:
            node = self._sceneManager.getRootSceneNode().createChildSceneNode("CamNode2", (0, 200, 400))
        node.createChildSceneNode("PitchNode2")

    ## Client methods

    def addEventListener(self, listenner):
        """ Register a event listener """
        self._subscribers.append(listenner)
    
    def removeEventListener(self, listenner):
        """ Remove a event listenner """
        self._subscribers.remove(listenner)

    def getRenderWindow(self):
        """ Returns a reference to the render window """
        return OgreWindow(self._renderWindow)
    
    def getSceneManager(self):
        return SceneManager(self._sceneManager)

    def getGUIGlueArgs(self):
        """ This gets required args to initialize and glue the GUI,
        should not be used for nothing else """
        return (self._renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 0, self._sceneManager)

    def getRendererFactory(self):
        return self._renderFactory

    def getCamera(self):
        return self._camera


class OgreWindow(object):
    
    def __init__(self, window):
        self._renderWindow = window
    
    def _getOgreRenderWindow(self):
        return self._renderWindow
        
    def getMetrics(self):
        #dir(self._renderWindow)
        #help(self._renderWindow.getMetrics)
        # Seems that I or upstream has broken getMetric
        w = 0
        h = 0
        c = 0
        l = 0
        t = 0
        w,h,c,l,t = self._renderWindow.getMetrics(w,h,c,l,t)
        return w,h,c,l,t

    def getStatistics(self):
        return self._renderWindow.getStatistics()

class SceneManager(object):
    
    def __init__(self, sceneManager):
        self._sceneManager = sceneManager
    
    def _getOgreSceneManager(self):
        return self._sceneManager

    def setAmbientLight(self,a):
        self._sceneManager.ambientLight = a


class Frame(object):
    
    def __init__(self, frameevt):
        self._frameevt = frameevt
        self.timeSinceLastFrame = frameevt.timeSinceLastFrame

class EventListener(ogre.FrameListener, ogre.WindowEventListener):
    
    def __init__(self, renderWindow, subscribers):
        ogre.FrameListener.__init__(self)
        ogre.WindowEventListener.__init__(self)
        self._subscribers = subscribers
        self._renderWindow = renderWindow
        self._window = OgreWindow(renderWindow)
    
    # Begin windon events
    def windowMoved(self, rw):
        ev = Event(EventType.WIN_MOVED,self._window)
        for s in self._subscribers:
            s.processEvent(ev)
    
    def windowResized(self, rw):
        ev = Event(EventType.WIN_RESIZED,self._window)
        for s in self._subscribers:
            s.processEvent(ev)

    def windowClosed(self, rw):
        ev = Event(EventType.WIN_CLOSED,self._window)
        for s in self._subscribers:
            s.processEvent(ev)

    def windowFocusChange(self, rw):
        ev = Event(EventType.WIN_FOCUS,self._window)
        for s in self._subscribers:
            s.processEvent(ev)
    
    # End window events
    
    # Begin Frame events
    def frameStarted(self, evt):
        if self._renderWindow.isClosed():
            return False
        ev = Event(EventType.FRAME_STARTED,Frame(evt))
        for s in self._subscribers:
            s.processEvent(ev)
        return True
    
    def frameEnded(self, evt):
        ev = Event(EventType.FRAME_ENDED,Frame(evt))
        for s in self._subscribers:
            s.processEvent(ev)
        return True
    
    # End Frame events
    
###########TO BE DELETED#########

class FrameListener(ogre.FrameListener, ogre.WindowEventListener):
    """A default frame listener, which takes care of basic mouse and keyboard
    input."""
      
    def __init__(self, renderWindow, camera, bufferedKeys = False, bufferedMouse = True, bufferedJoy = False):
        ogre.FrameListener.__init__(self)
        ogre.WindowEventListener.__init__(self)
        self.camera = camera
        self.renderWindow = renderWindow
        self.statisticsOn = True
        self.numScreenShots = 0
        self.timeUntilNextToggle = 0
        self.sceneDetailIndex = 0
        self.moveScale = 0.0
        self.rotationScale = 0.0
        self.translateVector = ogre.Vector3(0.0,0.0,0.0)
        self.filtering = ogre.TFO_BILINEAR
        self.moveSpeed = 100.0
        self.rotationSpeed = 8.0
        self.displayCameraDetails = False
        
    def __del__ (self ):
        ogre.WindowEventUtilities.removeWindowEventListener(self.renderWindow, self)
        self.windowClosed(self.renderWindow)

    def windowClosed(self, rw):
      #Only close for window that created OIS (mWindow)
      if( rw == self.renderWindow ):
         if( self.InputManager ):
            self.InputManager.destroyInputObjectMouse( self.Mouse )
            self.InputManager.destroyInputObjectKeyboard( self.Keyboard )
            if self.Joy:
                self.InputManager.destroyInputObjectJoyStick( self.Joy )
            OIS.InputManager.destroyInputSystem(self.InputManager)
            self.InputManager=None
            
    def frameStarted(self, frameEvent):
        if self.timeUntilNextToggle >= 0:
            self.timeUntilNextToggle -= frameEvent.timeSinceLastFrame
    
        if frameEvent.timeSinceLastFrame == 0:
            self.moveScale = 1
            self.rotationScale = 0.1
        else:
            self.moveScale = self.moveSpeed * frameEvent.timeSinceLastFrame
            self.rotationScale = self.rotationSpeed * frameEvent.timeSinceLastFrame
    
        self.rotationX = ogre.Degree(0.0)
        self.rotationY = ogre.Degree(0.0)
        self.translateVector = ogre.Vector3(0.0, 0.0, 0.0)
        if not self._processUnbufferedKeyInput(frameEvent):
            return False
        
        if not self.MenuMode:   # if we are in Menu mode we don't move the camera..
            self._processUnbufferedMouseInput(frameEvent)
            self._moveCamera()
        return True

    def _processUnbufferedKeyInput(self, frameEvent):
        if self.Keyboard.isKeyDown(OIS.KC_A):
            self.translateVector.x = -self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_D):
            self.translateVector.x = self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_UP) or self.Keyboard.isKeyDown(OIS.KC_W):
            self.translateVector.z = -self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_DOWN) or self.Keyboard.isKeyDown(OIS.KC_S):
            self.translateVector.z = self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_PGUP):
            self.translateVector.y = self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_PGDOWN):
            self.translateVector.y = - self.moveScale

        if self.Keyboard.isKeyDown(OIS.KC_RIGHT):
            self.rotationX = - self.rotationScale

        if self.Keyboard.isKeyDown(OIS.KC_LEFT):
            self.rotationX = self.rotationScale

        if self.Keyboard.isKeyDown(OIS.KC_ESCAPE) or self.Keyboard.isKeyDown(OIS.KC_Q):
            return False

        if( self.Keyboard.isKeyDown(OIS.KC_F) and self.timeUntilNextToggle <= 0 ): 
             self.statisticsOn = not self.statisticsOn
             self.showDebugOverlay(self.statisticsOn)
             self.timeUntilNextToggle = 1

        if self.Keyboard.isKeyDown(OIS.KC_T) and self.timeUntilNextToggle <= 0:
            if self.filtering == ogre.TFO_BILINEAR:
                self.filtering = ogre.TFO_TRILINEAR
                self.Aniso = 1
            elif self.filtering == ogre.TFO_TRILINEAR:
                self.filtering = ogre.TFO_ANISOTROPIC
                self.Aniso = 8
            else:
                self.filtering = ogre.TFO_BILINEAR
                self.Aniso = 1

            ogre.MaterialManager.getSingleton().setDefaultTextureFiltering(self.filtering)
            ogre.MaterialManager.getSingleton().setDefaultAnisotropy(self.Aniso)
            self.showDebugOverlay(self.statisticsOn)
            self.timeUntilNextToggle = 1
        
        if self.Keyboard.isKeyDown(OIS.KC_SYSRQ) and self.timeUntilNextToggle <= 0:
            path = 'screenshot_%d.png' % self.numScreenShots
            self.numScreenShots += 1
            self.renderWindow.writeContentsToFile(path)
            Application.debugText = 'screenshot taken: ' + path
            self.timeUntilNextToggle = 0.5
        
        if self.Keyboard.isKeyDown(OIS.KC_R) and self.timeUntilNextToggle <= 0:
            detailsLevel = [ ogre.PM_SOLID,
                             ogre.PM_WIREFRAME,
                             ogre.PM_POINTS ]
            self.sceneDetailIndex = (self.sceneDetailIndex + 1) % len(detailsLevel)
            self.camera.polygonMode=detailsLevel[self.sceneDetailIndex]
            self.timeUntilNextToggle = 0.5
            
        if self.Keyboard.isKeyDown(OIS.KC_F) and self.timeUntilNextToggle <= 0:
            self.statisticsOn = not self.statisticsOn
            self.showDebugOverlay(self.statisticsOn)
            self.timeUntilNextToggle = 1
        
        if self.Keyboard.isKeyDown(OIS.KC_P) and self.timeUntilNextToggle <= 0:
            self.displayCameraDetails = not self.displayCameraDetails
            if not self.displayCameraDetails:
                Application.debugText = ""
                
        if self.displayCameraDetails:
            # Print camera details
            pos = self.camera.getDerivedPosition()
            o = self.camera.getDerivedOrientation()
            Application.debugText = "P: %.3f %.3f %.3f O: %.3f %.3f %.3f %.3f"  \
                        % (pos.x,pos.y,pos.z, o.w,o.x,o.y,o.z)
        return True        
        
    def _isToggleKeyDown(self, keyCode, toggleTime = 1.0):
        if self.Keyboard.isKeyDown(keyCode)and self.timeUntilNextToggle <=0:
            self.timeUntilNextToggle = toggleTime
            return True
        return False
        
    def _isToggleMouseDown(self, Button, toggleTime = 1.0): 
        ms = self.Mouse.getMouseState() 
        if ms.buttonDown( Button ) and self.timeUntilNextToggle <=0: 
            self.timeUntilNextToggle = toggleTime 
            return True 
        return False 

    def _processUnbufferedMouseInput(self, frameEvent):
        ms = self.Mouse.getMouseState()
        if ms.buttonDown( OIS.MB_Right ):
            self.translateVector.x += ms.X.rel * 0.13
            self.translateVector.y -= ms.Y.rel * 0.13
        else:
            self.rotationX = ogre.Degree(- ms.X.rel * 0.13)
            self.rotationY = ogre.Degree(- ms.Y.rel * 0.13)

    def _moveCamera(self):
        self.camera.yaw(self.rotationX)
        self.camera.pitch(self.rotationY)
        try:
            self.camera.translate(self.translateVector) # for using OgreRefApp
        except AttributeError:
            self.camera.moveRelative(self.translateVector)
