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
Example file, with basic Input that handles input action 'exit'
"""

__version__ = "$Revision$"

__all__ = []


class MyBasicInputHandler(object):
    
    def __init__(self,engine):
        self._engine = engine
        
    def onInputAction(self,action,args=None):
        
        if action=="exit":
            self._engine.Terminate()
        else:
            return False
        return True
