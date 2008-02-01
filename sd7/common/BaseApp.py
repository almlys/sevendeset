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


from MyDict import MyDict
from bootstrap.xmlparser import XMLParser


class BaseApplication(object):
    """
    Base Aplication, with configuration stuff, etc...
    Intended to be used with any type of GUI framework
    (Gtk, Qt, wxPython, Tk, CEGUI, etc...)
    """
    
    _options = MyDict() #: Defines app options
    _configFile = "config/config.xml" #: Defines the config file path

    def __init__(self,args = None):
        """
        @param args: App Args
        """
        if args!=None:
            self._parseArgs(args)
        self._readConfig()
        self._setCmdConfig()
        self._run(args)
    
    def _run(self,args=None):
        pass

    def _parseArgs(self,argv):
        n=len(argv)-1
        for i in xrange(1,n+1):
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
                    print "Ignoring Unknown Parameter %s" %(param,)
            else:
                print "Ignoring Unknown Parameter %s" %(param,)

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
            print """<?xml version='1.0' encoding='UTF-8' ?>
<!DOCTYPE sd7config SYSTEM "http://7d7.almlys.org/spec/draft/sd7Config.dtd">
<sd7config>
""" >> out
        for section in _options:
            if section == "cmd":
                # Hide command line options
                continue
            print "\t<section name='%s'>" %(section,) >> out
            for option in _options[section]:
                if option.startswith("_"):
                    continue
                print "\t\t<option name='%s' value='%s' />" %(option,_options[section][option]) >> out
            print "\t</section>" >> out
        print "</sd7config>" >> out
        out.close()

    def GetCfg(self,section,key):
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


