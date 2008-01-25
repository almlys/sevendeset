#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Defines the bootstrap module interface

"""


class BModule(object):
    """
    A Module
    """

    def getSource(self):
        """ Gets the latest source code version of this module """
        pass
    
    def updateSource(self):
        """ Updates the module source code """
        pass
    
    def removeSource(self):
        """ Removes all the source of this module """
        pass
    
    def applyPatch(self):
        """ Applyes a patch to the module source code """
        pass
    
    def build(self):
        """ Builds the module """
        pass
    
    def clean(self):
        """ Cleans the source tree module form binary objects """
        pass
    
    def install(self):
        """ Installs the module """
        pass
    
    def createPackage(self):
        """ Creates a package of this module? """
        pass



