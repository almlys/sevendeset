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
Base Application
"""

__version__ = "$Revision$"

__all__ = ['BaseApplication',]

import os.path
import sys

from MyDict import MyDict
from sdlogger import mlog
from bootstrap.xmlparser import XMLParser


class BaseApplication(object):
    """
    Base Aplication, with configuration stuff, etc...
    Intended to be used with any type of GUI framework
    (Gtk, Qt, wxPython, Tk, CEGUI, etc...)
    """
    
    _options = MyDict() #: Defines app options
    _configFile = "config/config.xml" #: Defines the config file path
    _old_stdout = None
    _old_stderr = None
    _logdir = 'log'
    _log = None
    _logerr = None

    def __init__(self,args = None,redirect=True):
        """
        Init app
        @param args: App Args
        @param redirect: Redirects stdout/stderr to log file
        """
        if args!=None:
            self._parseArgs(args)
        if os.path.isfile(self._configFile):
            self._readConfig()
        self._setCmdConfig()
        self._logdir = self.GetCfg('global','system.logdir')
        if redirect:
            self._log = mlog(sys.stdout,self._logdir + '/stdout.log','w')
            self._logerr = mlog(sys.stderr,self._logdir + '/stderr.log','w')
            self._old_stdout = sys.stdout
            self._old_stderr = sys.stderr
            sys.stdout = self._log
            sys.stderr = self._logerr
        else:
            self._log = sys.stdout
            self._logerr = sys.stderr
        
        self._installGettext()
    
    def __del__(self):
        self._saveConfig()
        if self._old_stdout != None:
            sys.stdout = self._old_stdout
            self._log.close()
        if self._old_stderr != None:
            sys.stderr = self._old_stderr
            self._logerr.close()
    
    def _parseArgs(self,argv):
        n=len(argv)-1
        i = 1
        while i <= n:
            param=argv[i]
            if param.startswith("-"):
                if param=="-c" and i<n:
                    i+=1
                    self._configFile=argv[i]
                elif param=="-o" and i<n-1:
                    i+=1
                    if not self._options.has_key("cmd"):
                        self._options["cmd"] = MyDict()
                    self._options["cmd"][argv[i]]=argv[i+1]
                    i+=1
                else:
                    i = self._parseArgument(argv,i,n)
            else:
                i = self._parseArgument(argv,i,n)
            i = i+1

    def _parseArgument(argv,i,n):
        print "Ignoring Unknown Parameter %s" %(argv[i],)

    def _readConfig(self):
        """Load App configuration"""
        if self._configFile!=None:
            self._config = XMLParser()
            self._config.readfile(self._configFile)
            
            for section in self._config.xsd7config[0].xsection:
                for option in section.xoption:
                    if not self._options.has_key(section.pname):
                        self._options[section.pname] = MyDict()
                    self._options[section.pname][option.pname] = option.pvalue
        
        self._setConfigDefaults()
    
    def _setConfigDefaults(self):
        """ Set the default configuration values """
        if self.GetCfg('global','app.gettext.locales') == None:
            self.SetCfg('global','app.gettext.locales','data/system/locales')
        if self.GetCfg('global','app.gettext.domain') == None:
            self.SetCfg('global','app.gettext.domain',self._getGettextDomain())
        if self.GetCfg('global','system.logdir') == None:
            self.SetCfg('global','system.logdir','log')
    
    def _getGettextDomain(self):
        return "Undefined"

    def _setCmdConfig(self):
        """
        Command line passed args, are more prioritary
        """
        if self._options.has_key("cmd"):
            for opt in self._options["cmd"]:
                self._options["global"][opt] = self._options["cmd"][opt]

    def _saveConfig(self, cfg = None):
        """Save App configuration"""
        if cfg == None:
            cfg = self._configFile
        if cfg != None:
            out = file(cfg,'w')
            out.write("""<?xml version='1.0' encoding='UTF-8' ?>
<!DOCTYPE sd7config SYSTEM "http://7d7.almlys.org/spec/draft/sd7Config.dtd">
<sd7config>

""")
        for section in self._options:
            if section == "cmd":
                # Hide command line options
                continue
            out.write("\t<section name='%s'>\n" %(section,))
            for option in self._options[section]:
                if option.startswith("_"):
                    continue
                out.write("\t\t<option name='%s' value='%s' />\n" %(option,self._options[section][option]))
            out.write("\t</section>\n\n")
        out.write("</sd7config>")
        out.close()

    def SetCfg(self,section,key,value):
        if not self._options.has_key(section):
            self._options[section] = MyDict()
        self._options[section][key] = value

    def GetCfg(self,section,key):
        """ Gets a configuration value """
        if self._options.has_key(section) and self._options[section].has_key(key):
            return self._options[section][key]
        return None

    def _installGettext(self,lang=None):
        """Installs GetText"""
        import gettext
        if lang == None:
            gettext.install(self.GetCfg("global","app.gettext.domain"),
                            self.GetCfg("global","app.gettext.locales"),True)
        else:
            gettext.translation(self.GetCfg("global","app.gettext.domain"),
                                self.GetCfg("global","app.gettext.locales"),
                                (lang,)).install(True)

    def GetLanguages(self):
        """ Returns all available languages """
        try:
            return self.__Languages
        except:
            import dircache
            self.__Languages={}
            # Dirty hardcoded ugly LangDict
            _ = lambda x : x
            LangDict={"en":_("English"),"es":_("Spanish"),"ca":_("Catalan")}
            for lan in dircache.listdir(self.GetCfg("global","app.gettext.locales")):
                if lan in LangDict:
                    self.__Languages[lan]=LangDict[lan]
                else:
                    self.__Languages[lan]=lan
            return self.__Languages

    def SetLanguage(self,lang):
        """ Sets the application language """
        #import locale
        #locale.setlocale(locale.LC_ALL, (lang,"utf-8"))
        self.__Language=lang
        self._installGettext(lang)

    def GetLanguage(self):
        """ Returns current application language """
        try:
            return self.__Language
        except:
            import locale
            self.__Language=locale.getdefaultlocale()[0][:2]
            return self.__Language

    def GetAppVersion(self):
        """ Returns thea application version """
        return "$Revision$"


