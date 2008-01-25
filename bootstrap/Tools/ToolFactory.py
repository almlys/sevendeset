#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project BootStrap
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#

class ToolNotInstalled(Exception): pass

class _ToolDownloadFactory(object):
    
    def __init__(self):
        self.tools = {}
        self.loadTools()
    
    def loadTools(self):
        import Tools
        #from Tools import WgetTool, CVSTool
        self.addTool("wget",Tools.WgetTool)
        self.addTool("cvs",Tools.CVSTool)
        self.addTool("svn",Tools.SVNTool)

    def addTool(self,name,klass):
        self.tools[name]=klass
    
    def create(self,name):
        if not self.tools.has_key(name):
            raise ToolNotInstalled,name
        return self.tools[name]()
    
    def get(self,name,args):
        #print args
        return self.create(name).get(args)

class _ToolFactory(object):
    
    def __init__(self):
        self.tools = {}
        self.loadTools()
    
    def loadTools(self):
        import Tools
        #self.addTool("wget",Tools.WgetTool)
        #self.addTool("cvs",Tools.CVSTool)
        self.addTool("mkdir",Tools.MkdirTool)
        self.addTool("cd",Tools.CdTool)

    def addTool(self,name,klass):
        self.tools[name]=klass
    
    def create(self,name):
        if not self.tools.has_key(name):
            raise ToolNotInstalled,name
        return self.tools[name]()
    
    def run(self,name,args):
        #print args
        return self.create(name).run(args)


_ToolDownloadFactoryInstance = None
_ToolFactoryInstance = None

def ToolDownloadFactory():
    global _ToolDownloadFactoryInstance

    if _ToolDownloadFactoryInstance == None:
        _ToolDownloadFactoryInstance = _ToolDownloadFactory()
    
    return _ToolDownloadFactoryInstance

def ToolFactory():
    global _ToolFactoryInstance

    if _ToolFactoryInstance == None:
        _ToolFactoryInstance = _ToolFactory()
    
    return _ToolFactoryInstance

