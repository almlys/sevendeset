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

__all__ = ["BuildError", "InstallError", "PatchError", "BootStrap", "MainApp"]


import os
import os.path
import sys
import random
import re

from xmlparser import XMLParser
from Tools import ToolDownloadFactory, ToolFactory, ToolError

class DownloadError(Exception):
    """
    Exception launched when a file cannot be downloaded from Internet
    """

class CommandError(Exception):
    """
    Error running a command
    """

class BuildError(Exception):
    """
    Error building module
    """

class InstallError(Exception):
    """
    Error installing a module
    """

class PatchError(Exception):
    """
    Error patching a module
    """

class CleanError(Exception):
    """
    Error cleanning a module
    """

class ModuleNotFoundError(Exception):
    """
    A module cannot be found!
    """

class UnsuportedPlatformError(Exception):
    """
    Raised on unsuported platforms
    """


class BootStrap(object):
    """
    Main BootStrap Class
    """

    _manifestFile = None #: Path to BootStrap manifest
    _manifest = XMLParser() #: The manifest data
    _toolDownloadFactory = ToolDownloadFactory() #: Download factory
    _toolFactory = ToolFactory() #: Generic tool factory

    def __init__(self, options):
        """
        Init
        @param options: A dictonary containing all BootStrap options
        """
        self._platformDetect(options)
        self._configurePaths(options)
        self._configureEnv(options)

        self._manifestFile = options["global"]["BootStrap.manifest"]
        self._manifest.readfile(self._manifestFile)


    def _configurePaths(self, options):
        """
        Configures the applications paths
        """
        def setPath(path):
            """"
            Sets path
            @param path
            """
            if path.startswith('/'):
                return path
            else:
                return os.getcwd() + '/' + path.strip("./")

        self._downloadPath = \
            setPath(options["global"]["BootStrap.downloadPath"])
        self._outputPath = setPath(options["global"]["BootStrap.outputPath"])
        self._prefix = setPath(options["global"]["BootStrap.prefix"])
        self._patches = setPath(options["global"]["BootStrap.patches"])
        self._moduleStatus = \
            setPath(options["global"]["BootStrap.moduleStatus"])
        self._branch = options["global"]["BootStrap.branch"]
        
        if not os.path.exists(self._downloadPath):
            os.makedirs(self._downloadPath, 0755)
        if not os.path.exists(self._outputPath):
            os.makedirs(self._outputPath, 0755)
        if not os.path.exists(self._prefix):
            os.makedirs(self._prefix, 0755)
        if not os.path.exists(self._prefix + "/lib64") and \
            self._arch == 'x86_64':
            if not os.path.exists(self._prefix + "/lib"):
                os.makedirs(self._prefix+"/lib", 0755)
            os.symlink(self._prefix+"/lib", self._prefix + "/lib64")

    def _configureEnv(self, options):
        """
        Configures the application environment
        """
        # Enviorment vars
        prefix = os.environ['PREFIX'] = self._prefix

        version = sys.version_info
        version = str(version[0]) + "." + str(version[1])
        self._python_version = version

        a, b = os.popen4("gcc -v")
        self._gcc_version = "".join(re.search('gcc.* ([0-9]*\.[0-9]*)',
            b.read()).group(1).split("."))
        os.environ['MY_GCC_VERSION'] = self._gcc_version

        os.environ['PATH'] = prefix + '/bin:' + os.environ['PATH']

        def setEnv(key, val, sep = ":"):
            aux = ""
            if os.environ.has_key(key):
                aux = sep + os.environ[key]
            os.environ[key] = val + aux

        setEnv('LD_LIBRARY_PATH', prefix + '/lib')
        setEnv('PYTHONPATH',
            os.getcwd() + ":" + prefix + '/lib/python' + \
            version + '/site-packages')

        setEnv('CPPFLAGS', '-I' + prefix + '/include', " ")
        setEnv('LDFLAGS', '-L' + prefix + '/lib', " ")
        setEnv('PKG_CONFIG_PATH', prefix + '/lib/pkgconfig')

    def _platformDetect(self, options):
        """
        Detects and sets the current architecture and platform details
        """

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
                # Sanity check
                import struct
                bytes = struct.calcsize('P')
                self._arch = os.uname()[4]
                if self._arch == 'x86_64' and bytes != 8:
                    raise UnsuportedPlatformError,"""
It looks like you are running a 64 bits kernel, but your user-space applications
are compiled as 32 bits. You are attempting to build a 64 binary with a 32 bits
compiler and, as far as I know, that it is not possible.
In order to avoid this warning, you may launch this script under the shell
created by 'linux32'.
Check documentation of the 'linux32' or the 'util-linux' Debian/Ubuntu packages
"""
            else:
                # Needs to be ported (defaulting to 32 bits)
                self._arch = "i686"
        # End Platform stuff (Move this code to another place)

    def _searchModule(self,moduleName):
        """
        Returns the module associated to a Name
        @param moduleName the module
        """
        for module in self._manifest.xbootstrap[0].xmodule:
            if hasattr(module,"pignore") and module.pignore == "yes":
                continue
            if module.pname == moduleName:
                return module
        raise ModuleNotFoundError,moduleName

    def getDefaultTarget(self):
        """
        Returns the default target module
        """
        if hasattr(self._manifest.xbootstrap[0], "pdefault_target"):
            return self._manifest.xbootstrap[0].pdefault_target
        return None


    def _mget(self,module,update=False,redownload=False):
        """
        Downloads a module, using the specified method
        @param module: Module node object got from XMLParser
        @param update: If true it will update the module code
        (only for SVN/CVS modules) downloaded code will be unpacked again
        @param redownload: If true it will download again the entire code
        from scratch
        """
        
        # Architecture/Platform stuff
        wget_sources = []
        svn_sources = []
        for source in module.xsource:
            if hasattr(source,"pplatform") and source.pplatform!=self._platform:
                continue
            if hasattr(source,"parch") and source.parch!=self._arch:
                continue
            if hasattr(source,"ppython") and \
                source.ppython!=self._python_version:
                continue
            if hasattr(source,"pbranch") and source.pbranch!=self._branch:
                continue
            if source.pmethod=='wget':
                wget_sources.append(source)
            else:
                svn_sources.append(source)
        if len(wget_sources) == 0 and len(svn_sources) == 0:
            info = sys.platform
            if hasattr(os,"uname"):
                info += " " + " ".join(os.uname())
            info += " Python " + self._python_version
            raise UnsuportedPlatformError,info
        # End architecture/Platform stuff
        
        used_sources = []
        while len(wget_sources) != 0 or len(svn_sources) != 0:
            if len(wget_sources) == 0:
                wget_sources = svn_sources
                svn_sources = []
            if len(wget_sources) != 0:
                source = wget_sources[int(random.random() * len(wget_sources))]
                wget_sources.remove(source)
                try:
                    self._mget_inner(module,source,update,redownload)
                except ToolError,e:
                    print e
                    print "Cannot download from that source,\
attempting another one"
                    continue
                return
        raise DownloadError,"Cannot download from any suitable location"
        
    def _mget_inner(self,module,xsource,update,redownload):
        method = xsource.pmethod
        source = xsource.paddr
        args = xsource.attrs
        args['name'] = module.pname
        args['path'] = module.pname
        args['downloads'] = self._downloadPath
        args['output'] = self._outputPath
        args['update'] = update
        args['redownload'] = redownload

        print "Downloading %s from %s using %s" %(module.pname,source,method)
        tool = self._toolDownloadFactory.get(method,args)
    
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
                raise PatchError
                #pass
            f = file(check,"w")
            f.close()
            #os.utime(check,None)
            
        except PatchError,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)

    def patch(self,module_name,args=[]):
        self._mpatch(self._searchModule(module_name))

    def _run_cmd(self,module,family):
        """
        Runs a command
        @param module The module name
        @family Family can be, build, install and clean
        @returns True if commands were succesfully run
        @throws Exception On command error
        """
        xfamily = "x" + family
        if not hasattr(module,xfamily):
            return False
        cdir = os.getcwd()
        try:
            os.chdir(self._outputPath + '/' + module.pname)
            for cmd in getattr(module,xfamily)[0].xcmd:
                if hasattr(cmd,"pcmd"):
                    self._toolDownloadFactory.run(cmd.pcmd,cmd.attrs)
                elif (os.system(cmd.data)!=0):
                    raise CommandError,family + ":" + cmd.data
        except Exception,e:
            raise e
        finally:
            os.chdir(cdir)

    def _mbuild(self,module):
        """
        Runs build command batch
        """
        self._run_cmd(module,"build")

    def build(self,module_name,args=[]):
        """
        Builds the specified module
        """
        self._mbuild(self._searchModule(module_name))

    def _minstall(self,module):
        self._run_cmd(module,"install")

    def install(self,module_name,args=[]):
        self._minstall(self._searchModule(module_name))

    def _mclean(self,module):
        self._run_cmd(module,"clean")

    def clean(self,module_name,args=[]):
        self._mclean(self._searchModule(module_name))

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
        'BootStrap.manifest' : 'config/bootstrap.xml',
        'BootStrap.branch' : 'stable'
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
        @param args: App Args
        """
        if args!=None:
            self._parseArgs(args)
        self._readConfig()
        self._setCmdConfig()
        #print self._options
        self._bootStrap = BootStrap(self._options)
        self._runcmd()

    def _addCmdOption(self, key, value):
        """
        Adds a new command line option
        """
        if not self._options.has_key("cmd"):
            self._options["cmd"] = {}
        self._options["cmd"][key] = value


    def _parseArgs(self,argv):
        """
        Parse coniguration args
        @param argv: The args
        """
        n=len(argv)-1
        for i in xrange(1,n+1):
            param=argv[i]
            if param.startswith("-"):
                if param == "-c" and i < n:
                    i+=1
                    self._configFile=argv[i]
                elif param == "--prefix" and i < n:
                    i+= 1
                    self._addCmdOption("BootStrap.prefix", argv[i])
                elif param=="-o" and i < n-1:
                    i+= 1
                    self._addCmdOption(argv[i], argv[i+1])
                    i+=1
                else:
                    self._args.append(param)
            else:
                self._modules.append(param)
        if len(self._modules)!= 0:
            self._command = self._modules.pop(0)

    def _readConfig(self):
        """
        Reads the configuration file
        """
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

    def _runcmd(self):
        """
        Runs a cmd with args for the specified modules
        """
        cmd = self._command
        if cmd==None or cmd=="help":
            print """sd7 BootStrap Application
bootstrap/bootstrap.py [options] command <module1> <module2> <module3>
get <module1> <module2> ...     Downloads the module(s)
    -f : Forces re-download
update <module1> <module2> ...  Updates the module(s)
remove <module1> <module2> ...  Removes the module(s)
patch <module1> <module2> ...   Patches the module(s)
build <module1> <module2> ...   Builds the module(s)
clean <module1> <module2> ...   Cleans the module(s)
install <module1> <module2> ... Installs the module(s)
auto <module1> <module2> ...    Automatically builds and installs the module(s)
"""
            return
        if len(self._modules)==0:
            self._modules = [self._bootStrap.getDefaultTarget(),]

        for m in self._modules:
            if hasattr(self._bootStrap, cmd):
                getattr(self._bootStrap, cmd)(m, self._args)
            else:
                print "Unknown command %s" % (cmd,)


if __name__ == "__main__":
    import time
    start = time.time()
    app = MainApp(sys.argv)
    end = time.time()
    print "done in %.2f seconds" % (end-start,)

