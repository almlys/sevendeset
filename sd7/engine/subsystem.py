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

__all__ = ['SubSystem',]


import os
import time



class SubSystem(object):

    _config = None #: Configuration dict (reference to global section)
    _initialized = False #: Is the render engine initialized?
    _logDir = "log" #: Path to the log folder
    _name = None #: Subsystem name
    _debugmsg = False
    
    def __init__(self, subname = None, debug = True, options = None):
        if options!=None:
            self._config = options
        else:
            self._config = {}
        if subname == None:
            self._name = 'undefined'
        else:
            self._name = subname
        self._debugmsg = debug

    def _setConfigDefaults(self):
        """
        Sets default config parameters
        """
        if not self._config.has_key('system.logdir'):
            self._config['system.logdir'] = 'log'

    def _openLog(self):
        self._log = file(self._logDir + '/' + self._name + '.log','w')
    
    def _closeLog(self):
        self._log.close()
    
    def log(self,msg):
        self.logFile(msg)
        if self._debugmsg:
            print msg
    
    def logFile(self,msg):
        self._log.write(time.strftime('%Y:%m:%d:%H:%M:%S>') + msg + '\n')

    def initialize(self):
        """Initialize the render engine"""
        if self._initialized:
            raise "Cannot reinit"
        self._initialized = True
        self._setConfigDefaults()
        self._logFolder = self._config["system.logdir"]
        if not os.path.exists(self._logDir):
            os.mkdir(self._logDir)
        self._openLog()
        return True

    def isInitialized(self):
        return self._initialized

    def processEvent(self,evt):
        return True
