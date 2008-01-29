#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project BootStrap
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#

"""
sd7 Project BootStrap Script

This module downloads and build a set of libraries required to run sd7
"""

__version__ = "$Revision$"

__all__ = ["BuildError","InstallError","PatchError","BootStrap","MainApp"]


import os
import os.path
import sys

from xmlparser import XMLParser
from Tools import ToolDownloadFactory, ToolFactory


class BuildError(Exception): pass
class InstallError(Exception): pass
class PatchError(Exception): pass
class ModuleNotFoundError(Exception): pass
class UnsuportedPlatformError(Exception): pass


class BootStrap(object):
    """
    Main BootStrap Class
    """
    
    _manifestFile = None #: Path to BootStrap manifest
    _manifest = None #: The manifest data
    _ToolDownloadFactory = ToolDownloadFactory()
    _ToolFactory = ToolFactory()

    def __init__(self,options):
        """
        Init
        @param options: A dictonary containing all BootStrap options
        """
        self._manifestFile = options["global"]["BootStrap.manifest"]
        self._manifest = XMLParser()
        self._manifest.readfile(self._manifestFile)

        def setPath(path):
            if path.startswith('/'):
                return path
            else:
                return os.getcwd() + '/' + path.strip("./")


        self._downloadPath = setPath(options["global"]["BootStrap.downloadPath"])
        self._outputPath = setPath(options["global"]["BootStrap.outputPath"])
        self._prefix = setPath(options["global"]["BootStrap.prefix"])
        self._patches = setPath(options["global"]["BootStrap.patches"])
        self._moduleStatus = setPath(options["global"]["BootStrap.moduleStatus"])
        
        # Set Platform and architecture details
        if options["global"].has_key("BootStrap.platform"):
            self._platform = options["global"]["BootStrap.platform"]
        else:
            if sys.platform == "linux2":
                self._platform = "linux"
            else:
                self._platform = sys.platform
        if options["global"].has_key("BootStrap.arch"):
            self._arch = options["global"]["BootStrap.arch"]
        else:
            if hasattr(os,"uname"):
                self._arch = os.uname()[4]
            else:
                # Needs to be ported (defaulting to 32 bits)
                self._arch = "i686"
        # End Platform stuff (Move this code to another place)

        if not os.path.exists(self._downloadPath):
            os.makedirs(self._downloadPath,0755)
        if not os.path.exists(self._outputPath):
            os.makedirs(self._outputPath,0755)
        if not os.path.exists(self._prefix):
            os.makedirs(self._prefix,0755)

        # Enviorment vars
        prefix = os.environ['PREFIX'] = self._prefix

        version = sys.version.split('.')
        version = version[0] + "." + version[1]

        os.environ['PATH'] = prefix + '/bin:' + os.environ['PATH']
        os.environ['LD_LIBRARY_PATH'] = prefix + '/lib'
        os.environ['PYTHONPATH'] = os.getcwd() + ":" + prefix + '/lib/python' + version + '/site-packages'
        os.environ['CPPFLAGS'] = '-I' + prefix + '/include'
        os.environ['LDFLAGS'] = '-L' + prefix + '/lib'
        os.environ['PKG_CONFIG_PATH'] = prefix + '/lib/pkgconfig'
    
##    def run(self):
##        p = XMLParser()
##        p.readfile(self.config)
##        
##        for module in p.xbootstrap[0].xmodule:
##            if hasattr(module,"pignore") and module.pignore=="yes":
##                continue
##            self._mget(module,update=True)
##            self._mpatch(module)
##            self._mbuild(module)
##            self._minstall(module)

    def _searchModule(self,moduleName):
        """
        Returns the module associated to a Name
        """
        for module in self._manifest.xbootstrap[0].xmodule:
            if hasattr(module,"pignore") and module.pignore == "yes":
                continue
            if module.pname == moduleName:
                return module
        raise ModuleNotFoundError,moduleName

    def _mget(self,module,update=False,redownload=False):
        """
        Downloads a module, using the specified method
        @param module: Module node object got from XMLParser
        @param update: If true it will update the module code
        (only for SVN/CVS modules) downloaded code will be unpacked again
        @param redownload: If true it will download again the entire code from scratch
        """
        
        # Architecture/Platform stuff
        source = None
        for source in module.xsource:
            if hasattr(source,"pplatform") and source.pplatform!=self._platform:
                continue
            if hasattr(source,"parch") and source.parch!=self._arch:
                continue
            break
        if source == None:
            info = sys.platform()
            if hasattr(os.uname):
                info += " ".join(os.uname())
            raise UnsupportedPlatformError,info
        # End architecture/Platform stuff
        
        method = module.xsource[0].pmethod
        source = module.xsource[0].paddr
        args=module.xsource[0].attrs
        args['name'] = module.pname
        args['path'] = module.pname
        args['downloads'] = self._downloadPath
        args['output'] = self._outputPath
        args['update'] = update
        args['redownload'] = redownload

        print "Downloading %s from %s using %s" %(module.pname,source,method)
        tool = self._ToolDownloadFactory.get(method,args)
    
    def get(self,module_name,args=[]):
        if "-f" in args:
            redownload = True
        else:
            redownload = False
        self._mget(self._searchModule(module_name),False,redownload)

    def update(self,module_name,args=[]):
        self._mget(self._searchModule(module_name),True)

    def _mpatch(self,module):
        
        # Re do this, please!!
        
        if not hasattr(module,'xpatch'):
            return
        check = self._outputPath + '/' + module.pname + '/.bootstrap.patched'
        if os.path.exists(check):
            print "%s Already patched!" %(module.pname,)
            return
        cdir = os.getcwd()
        try:
            source = self._patches + '/' + module.xpatch[0].paddr
            os.chdir(self._outputPath + '/' + module.pname)
            print "Patching %s" %(source,)
            if (os.system("patch -N -i %s -p1" %(source,))!=0):
                #raise PatchError
                pass
            f = file(check,"w")
            f.close()
            #os.utime(check,None)
            
        except PatchError,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)

    def patch(self,module_name,args=[]):
        self._mpatch(self._searchModule(module_name))

    def _mbuild(self,module):
        if not hasattr(module,"xbuild"):
            return
        cdir = os.getcwd()
        try:
            os.chdir(self._outputPath + '/' + module.pname)
            for cmd in module.xbuild[0].xcmd:
                if hasattr(cmd,"pcmd"):
                    self._ToolFactory.run(cmd.pcmd,cmd.attrs)
                elif (os.system(cmd.data)!=0):
                    raise BuildError
        except Exception,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)

    def build(self,module_name,args=[]):
        self._mbuild(self._searchModule(module_name))

    def _minstall(self,module):
        if not hasattr(module,"xinstall"):
            return
        cdir = os.getcwd()
        try:
            os.chdir(self._outputPath + '/' + module.pname)
            for cmd in module.xinstall[0].xcmd:
                if hasattr(cmd,"pcmd"):
                    self._ToolFactory.run(cmd.pcmd,cmd.attrs)
                elif (os.system(cmd.data)!=0):
                    raise InstallError
        except Exception,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)

    def install(self,module_name,args=[]):
        self._minstall(self._searchModule(module_name))

    def auto(self,module_name,args=[]):
        self.get(module_name)
        self.patch(module_name)
        self.build(module_name)
        self.install(module_name)


class MainApp(object):
    """
    Main BootStrap Application
    """
    
    _args = [] #: Defines extra args to be appened to the cmd
    _options = { 'global' : {
        'BootStrap.downloadPath' : 'downloads',
        'BootStrap.outputPath' : 'depends',
        'BootStrap.prefix' : 'runtime',
        'BootStrap.patches' : 'patches',
        'BootStrap.moduleStatus' : 'BootStrap.status.xml',
        'BootStrap.manifest' : 'config/bootstrap.xml'
        }} #: Store all options (init to defaults)
    _configFile = None #: Defines configuration file
    _modules = [] #: The list of modules were bootstrap operates
    _command = None #: The command to run
    _config = None
    _bootStrap = None #: An instance of the BootStrap class
    
    def __init__(self,args=None):
        """
        @param args: App Args
        """
        self._run(args)
    
    def _run(self,args=None):
        """
        Run it
        """
        if args!=None:
            self._parseArgs(args)
        self._readConfig()
        self._setCmdConfig()
        #print self._options
        self._bootStrap = BootStrap(self._options)
        self._runcmd(self._command,self._args,self._modules)

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
                        self._options["cmd"] = {}
                    self._options["cmd"][argv[i]]=argv[i+1]
                    i+=1
                else:
                    self._args.append(param)
            else:
                self._modules.append(param)
        if len(self._modules)!=0:
            self._command = self._modules.pop(0)

    def _readConfig(self):
        if self._configFile!=None:
            self._config = XMLParser()
            self._config.readfile(self._configFile)
            
            for section in self._config.xsd7config[0].xsection:
                for option in section.xoption:
                    if not self._options.has_key(section.pname):
                        self._options[section.pname] = {}
                    self._options[section.pname][option.pname] = option.pvalue
    
    def _setCmdConfig(self):
        """
        Command line passed args, are more prioritary
        """
        if self._options.has_key("cmd"):
            for opt in self._options["cmd"]:
                self._options["global"][opt] = self._options["cmd"][opt]

    def _runcmd(self,cmd,args,modules):
        """
        Runs a cmd with args for the specified modules
        """
        if cmd==None or cmd=="help":
            print """sd7 BootStrap Application
get <module1> <module2> ...     Downloads the module(s)
update <module1> <module2> ...  Updates the module(s)
remove <module1> <module2> ...  Removes the module(s)
patch <module1> <module2> ...   Patches the module(s)
build <module1> <module2> ...   Builds the module(s)
clean <module1> <module2> ...   Cleans the module(s)
install <module1> <module2> ... Installs the module(s)
auto <module1> <module2> ...    Automatically builds and installs the module(s)
"""
            return
        if len(modules)==0:
            print "ToDo"
        else:
            for m in modules:
                if cmd=="get":
                    self._bootStrap.get(m,self._args)
                elif cmd=="update":
                    self._bootStrap.update(m)
                elif cmd=="remove":
                    self._bootStrap.remove(m)
                elif cmd=="patch":
                    self._bootStrap.patch(m)
                elif cmd=="build":
                    self._bootStrap.build(m)
                elif cmd=="clean":
                    self._bootStrap.clean(m)
                elif cmd=="install":
                    self._bootStrap.install(m)
                elif cmd=="auto":
                    self._bootStrap.auto(m)
                else:
                    print "Unknown command %s" %(cmd,)


if __name__ == "__main__":
    import time
    start = time.time()
    app = MainApp(sys.argv)
    end = time.time()
    print "done in %.2f seconds" %(end-start,)

