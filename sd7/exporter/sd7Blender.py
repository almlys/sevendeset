#!BPY
# -*- coding: utf-8 -*-
#
#    sd7 Project Engine
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#

"""
Name: 'sd7 Exporter (ogre)'
Blender: 247
Group: 'Export'
Tooltip: 'sd7 Engine Exporter (Ogre renderer version)'
"""

__author__ = "Alberto Montañola Lacort"
__version__ = "$Revision$"
__url__ = ['Author\' blog, http://almlys.org',
           'sd7 Project page, http://7d7.almlys.org',
           'sd7 Forum, http://forum.almlys.org']
__bpydoc__ = "This script will export all objects from your scene to the format used by sd7"


__all__ = []


import sys

try:
    import Blender
except ImportError:
    print "This script only runs inside Blender"
    sys.exit()

from Blender import Registry

from common.sdlogger import mlog


class sd7Exporter(object):
    """Main APP"""

    #def __init__(self):
        #self._config = Registry.GetKey("sd7Exporter")
        #if self._config == None:
        #    self._config = {}

    def open_file(self,filename):
        try:
            import psyco
            psyco.profile()
        except ImportError:
            print "Psyco not found"
        self._start = time.clock()
        print "Export to " + filename
        self.export_scene(filename)

    #def __del__(self):
        #Registry.SetKey("


if __name__ == '__main__':

    exp = sd7Exporter()
    
    #fname = Blender.sys.makename(ext = ".7xml")

    fname = "data/system/common/test.7xml"
    
    Blender.Window.FileSelector(exp.open_file, "Main description file", fname)

