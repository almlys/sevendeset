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
Defines the common RendererInterface
"""

__version__ = "$Revision$"

__all__ = ["RendererInterface"]


class RendererInterface(object):
    
    def __init__(self,options=None):
        """
        Init
        @param options: A dictionary with specific renderer options
        """
        pass
    
    def renderLoop(self):
        pass

