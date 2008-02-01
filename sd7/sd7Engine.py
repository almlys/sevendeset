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
    
    pass


if __name__ == '__main__':
    app = MainApp(sys.argv)

raise "stop"

_config = XMLParser()
_config.readfile("config/config.xml")
_options = MyDict()
    
for section in _config.xsd7config[0].xsection:
    for option in section.xoption:
        if not _options.has_key(section.pname):
            _options[section.pname] = MyDict()
        _options[section.pname][option.pname] = option.pvalue

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


print """<?xml version='1.0' encoding='UTF-8' ?>
<!DOCTYPE sd7config SYSTEM "http://7d7.almlys.org/spec/draft/sd7Config.dtd">
<sd7config>
"""

for section in _options:
    if section == "cmd":
        # Hide command line options
        continue
    print "\t<section name='%s'>" %(section,)
    for option in _options[section]:
        if option.startswith("_"):
            continue
        print "\t\t<option name='%s' value='%s' />" %(option,_options[section][option])
    print "\t</section>"

print "</sd7config>"

print "App Terminated"
