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

__all__ = ["GUI"]

from sd7.engine.controller import Controller


class GUI(Controller):
    
    __name__ = "GUI"
    
    def __init__(self,params):
        Controller.__init__(self,params)
        print params

    def initialize(self):
        Controller.initialize(self)
        self.log("Initializing %s" %(self.__name__))
        self._loadResources()
        self._loadMainGUI()
    
    def _loadResources(self):
        pass
    
    def _loadMainGUI(self):
        pass
        
    