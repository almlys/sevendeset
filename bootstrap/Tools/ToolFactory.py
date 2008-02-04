#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project BootStrap
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#


"""
Tool Factory Stuff

Manages the available tools
"""

__version__ = "$Revision$"

__all__ = ["ToolDownloadFactory","ToolFactory"]


import Tools
from Tools import ToolNotInstalled


class _ToolDownloadFactory(object):
    
    def __init__(self):
        self.tools = {}
        self.loadTools()
    
    def loadTools(self):
        #from Tools import WgetTool, CVSTool
        self.addTool("wget",Tools.WgetTool2)
        self.addTool("cvs",Tools.CVSTool)
        self.addTool("svn",Tools.SVNTool)

    def addTool(self,name,klass):
        self.tools[name]=klass
    
    def create(self,name):
        if not self.tools.has_key(name):
            raise ToolNotInstalled,name
        return self.tools[name]()
    
    def get(self,name,args):
        """
        Downloads/updates the selected source with the specified method
        @param name: Method/Tool to download the code
        @param args: Tuple of arguments passed to the inner tool
        """
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
        """
        Runs the specified tool with the inner params
        @param name: Name of the tool/cmd to run
        @param args: Inner params to send to the tool
        """
        #print args
        return self.create(name).run(args)



_ToolDownloadFactoryInstance = None
_ToolFactoryInstance = None


def ToolDownloadFactory():
    """
    Returns a ToolDownloadFactory instance
    """
    global _ToolDownloadFactoryInstance

    if _ToolDownloadFactoryInstance == None:
        _ToolDownloadFactoryInstance = _ToolDownloadFactory()
    
    return _ToolDownloadFactoryInstance


def ToolFactory():
    """
    Returns a ToolFactory instance
    """
    global _ToolFactoryInstance

    if _ToolFactoryInstance == None:
        _ToolFactoryInstance = _ToolFactory()
    
    return _ToolFactoryInstance

