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
    
    def __init__(self,argv):
        BaseApplication.__init__(self,argv)
    
    def _getGettextDomain(self):
        return "sd7Engine"
    
    def run(self):
        try:
            self._options['global']['_window.name'] = self.GetAppVersion()
            e = Engine(self._options)
            e.run()
        except:
            import traceback
            trace = file(self.GetCfg('global','system.logdir') + '/traceback.log','w')
            traceback.print_exc(file=trace)
            trace.close()
            traceback.print_exc(file=sys.stderr)
            try:
                import wx
                app = wx.App(redirect=False)
                wx.MessageBox(traceback.format_exc(),'Traceback - ' + self.GetAppVersion(),wx.ICON_ERROR)
            except ImportError:
                pass

    def GetAppVersion(self):
        return "sd7 Alchera pre-alpha v0.1 $Revision$"

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
    print "App Terminated"
