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

__all__ = ["MainApp","runsd7"]

import sys
import os

from common.BaseApp import BaseApplication
from sd7.engine import Engine


class MainApp(BaseApplication):
    
    def __init__(self,argv):
        BaseApplication.__init__(self,argv)
    
    def _getGettextDomain(self):
        return "sd7Engine"
    
    def run(self):
        try:
            self._options['global']['_window.name'] = self.getAppVersion()
            print "Startup...."
            e = Engine(self._options)
            print "Run..."
            e.run()
            print "END OK"
        except:
            import traceback
            traceback.print_exc(file=sys.stderr)
            if not os.path.exists(self.getCfg('global','system.logdir')):
                os.mkdir(self.getCfg('global','system.logdir'))
            trace = file(self.getCfg('global','system.logdir') + '/traceback.log','w')
            traceback.print_exc(file=trace)
            trace.close()
            return
            try:
                import wx
                app = wx.App(redirect=False)
                wx.MessageBox(traceback.format_exc(),'Traceback - ' + self.getAppVersion(),wx.ICON_ERROR)
            except ImportError:
                pass

    def getAppVersion(self):
        return "sd7 Alchera pre-alpha v0.1 $Revision$"

def runsd7():
    try:
        app = MainApp(sys.argv)
        app.run()
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
        try:
            if not os.path.exists('log'):
                os.mkdir('log')
            trace = file("log/traceback.log","w")
            traceback.print_exc(file=trace)
            trace.close()
        except:
            pass
        try:
            import wx
            app = wx.App(redirect=False)
            wx.MessageBox(traceback.format_exc(),"Traceback",wx.ICON_ERROR)
        except ImportError:
            pass
    print "App Terminated"

if __name__ == '__main__':
    runsd7()
