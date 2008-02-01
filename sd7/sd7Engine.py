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

import sys
from bootstrap.xmlparser import XMLParser
from common.BaseApp import BaseApplication
from sd7.engine import Engine


class MainApp(BaseApplication):
    
    def _getGettextDomain(self):
        return "sd7Engine"


if __name__ == '__main__':
    try:
        app = MainApp(sys.argv)
        app.run()
    except:
        import traceback
        try:
            trace = file("log/traceback.log","w")
            traceback.print_exc(file=trace)
            trace.close()
        except:
            pass
        traceback.print_exc(file=sys.stderr)
        try:
            import wx
            app = wx.App(redirect=False)
            wx.MessageBox(traceback.format_exc(),"Traceback",wx.ICON_ERROR)
        except ImportError:
            pass
raise "stop"


try:
    e = Engine(_options)
    e.run2()
except:
    import traceback, sys
    trace = file("log/traceback.log","w")
    traceback.print_exc(file=trace)
    trace.close()
    traceback.print_exc(file=sys.stderr)
    try:
        import wx
        app = wx.App(redirect=False)
        wx.MessageBox(traceback.format_exc(),"Traceback",wx.ICON_ERROR)
    except ImportError:
        pass


print "App Terminated"
