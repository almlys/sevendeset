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

__all__ = ["MouseButton"]

class MouseButton(object):

    LEFT = 0
    RIGHT = 1
    MIDDLE = 2
    X1 = 3
    X2 = 4

    butts = ["LEFT", "RIGHT", "MIDDLE", "X1", "X2"]

    @staticmethod
    def toString(id):
        return MouseButton.butts[id]

