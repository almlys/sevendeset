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

__all__ = ["HookMgr"]

from sd7.engine.subsystem import SubSystem as SubSystem
from bootstrap.xmlparser import XMLParser


class HookNotFoundError(Exception): pass

class HookMgr(SubSystem):
    
    __controller_map = {}
    __controller_cache = {}
    __autostart_list = []
    
    def __init__(self,options=None):
        """
        @param options: Set of options to configure the GUI
        @param type: String with the type of renderer, Ogre is the only currently one allowed
        @param args: Specific arguments of the renderer, required to glue both systems
        """
        SubSystem.__init__(self,'HookMgr',True,options)

    def __del__(self):
        self.stopAutomaticControllers()

    def initialize(self):
        SubSystem.initialize(self)
        self.log("Initializing HookManager")
        self.__loadMapping(self._config["system.hooks"])

    def __addController(self,name,classname,args):
        self.__controller_map[name] = (classname,args)
        
    def __saveControllerToCache(self,name,klass):
        self.__controller_cache[name] = klass
    
    def __loadMapping(self,file):
        xml = XMLParser()
        xml.readfile(file)
        
        for c in xml.xsd7hooks[0].xcontroller:
            print "Loading binding %s for %s" %(c.pbind,c.pname)
            params = {}
            if hasattr(c,"xparam"):
                for p in c.xparam:
                    print "  %s : %s" %(p.pname,p.data)
                    params[p.pname] = p.data
            if hasattr(c,"pautostart") and c.pautostart.lower()=="true":
                self.__autostart_list.append(c.pname)
            self.__addController(c.pname,c.pbind,params)

    def getController(self,name):
        """
        Returns the Controller class instance for the specified Binding
        @param name The controller class to instanciate
        """
        if self.__controller_cache.has_key(name):
            return self.__controller_cache[name]
        elif self.__controller_map.has_key(name):
            ctrl, params = self.__controller_map[name]
            path = ".".join(ctrl.split(".")[:-1])
            klass = ctrl.split(".")[-1]
            try:
                module = __import__(path, globals(), locals(), [klass,])
                kls = getattr(module, klass)(params)
                kls.setLogFunc(self.log)
                self.__saveControllerToCache(name,kls)
                return kls
            except ImportError,e:
                raise HookNotFoundError,"Cannot find %s:%s" %(name,ctrl)
        return None
    
    def destroyController(self,name):
        # If reference count gets to 0 it will be destroyed...
        self.__controller_cache.pop(name)

    def startAutomaticControllers(self):
        for c in self.__autostart_list:
            self.getController(c).initialize()
    
    def stopAutomaticControllers(self):
        for c in self.__autostart_list.reverse():
            self.destroyController(c)
