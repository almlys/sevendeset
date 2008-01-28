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
sd7 Main Entry Point file and Application
"""

__version__ = "$Revision$"

__all__ = []

from sd7.engine import Engine

e = Engine()
e.run()

print "App Terminated"
