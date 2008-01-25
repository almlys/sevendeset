#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project BootStrap
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#

import os, os.path

from xmlparser import XMLParser
from Tools import ToolDownloadFactory, ToolFactory

class BuildError(Exception): pass
class InstallError(Exception): pass
class PatchError(Exception): pass

class BootStrap(object):

    def __init__(self,options,config):
        self.config = config
        self.downloadFactory = ToolDownloadFactory()
        self.ToolFactory = ToolFactory()
        def setPath(path):
            if path.startswith('/'):
                return path
            else:
                return os.getcwd() + '/' + path.strip("./")
                
        self.downloadPath = os.getcwd() + '/' + 'downloads'
        self.outputPath = os.getcwd() + '/' + 'depends'
        self.prefix = os.getcwd() + '/' + 'runtime'
        self.patches = os.getcwd() + '/' + 'patches'
        fprefix = os.environ['PREFIX'] = self.prefix
        if not os.path.exists(self.downloadPath):
            os.makedirs(self.downloadPath,0755)
        if not os.path.exists(self.outputPath):
            os.makedirs(self.outputPath,0755)
        if not os.path.exists(self.prefix):
            os.makedirs(self.prefix,0755)
        import sys
        version = sys.version.split('.')
        version = version[0] + "." + version[1]
        # More enviorment vars
        os.environ['PATH']=fprefix + '/bin:' + os.environ['PATH']
        os.environ['LD_LIBRARY_PATH']=fprefix + '/lib'
        os.environ['PYTHONPATH']=fprefix + '/lib/python' + version + '/site-packages'
        os.environ['CPPFLAGS']='-I' + fprefix + '/include'
        os.environ['LDFLAGS']='-L' + fprefix + '/lib'
        os.environ['PKG_CONFIG_PATH']=fprefix + '/lib/pkgconfig'
    
    def run(self):
        p = XMLParser()
        p.readfile(self.config)
        
        for module in p.xbootstrap[0].xmodule:
            if hasattr(module,"pignore") and module.pignore=="yes":
                continue
            self._mget(module,update=True)
            self._mpatch(module)
            self._mbuild(module)
            self._minstall(module)


    def _mget(self,module,update=False,redownload=False):
        method = module.xsource[0].pmethod
        source = module.xsource[0].paddr
        args=module.xsource[0].attrs
        args['name'] = module.pname
        if 1 or not args.has_key('path'):
            args['path'] = module.pname
        args['downloads'] = self.downloadPath
        args['output'] = self.outputPath
        args['update'] = update
        args['redownload'] = redownload

        print "Downloading %s from %s using %s" %(module.pname,source,method)
        tool = self.downloadFactory.get(method,args)

    def _mpatch(self,module):
        if not hasattr(module,'xpatch'):
            return
        check = self.outputPath + '/' + module.pname + '/.bootstrap.patched'
        if os.path.exists(check):
            print "%s Already patched!" %(module.pname,)
            return
        cdir = os.getcwd()
        try:
            source = self.patches + '/' + module.xpatch[0].paddr
            os.chdir(self.outputPath + '/' + module.pname)
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


    def _mbuild(self,module):
        if not hasattr(module,"xbuild"):
            return
        cdir = os.getcwd()
        try:
            os.chdir(self.outputPath + '/' + module.pname)
            for cmd in module.xbuild[0].xcmd:
                if hasattr(cmd,"pcmd"):
                    self.ToolFactory.run(cmd.pcmd,cmd.attrs)
                elif (os.system(cmd.data)!=0):
                    raise BuildError
        except Exception,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)

    def _minstall(self,module):
        if not hasattr(module,"xinstall"):
            return
        cdir = os.getcwd()
        try:
            os.chdir(self.outputPath + '/' + module.pname)
            for cmd in module.xinstall[0].xcmd:
                if hasattr(cmd,"pcmd"):
                    self.ToolFactory.run(cmd.pcmd,cmd.attrs)
                elif (os.system(cmd.data)!=0):
                    raise InstallError
        except Exception,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)





class MainApp(object):
    
    _args = []
    _options = {}
    _options_defaults = {
        'BootStrap.downloadPath' : 'downloads',
        'BootStrap.outputPath' : 'depends',
        'BootStrap.prefix' : 'runtime',
        'BootStrap.patches' : 'patches',
        'BootStrap.cache' : 'depends/cache.status.xml',
        'BootStrap.manifest' : 'bootstrap.xml'
        }
    _configFile = None
    _modules = []
    _command = None
    _config = None
    _bootStrap = None
    
    def __init__(self):
        self._run()
    
    def _run(self):
        self._parseArgs()
        self._readConfig()
        self._bootStrap = BootStrap(self._options,self._configFile)
        self._runcmd(self._command,self._args,self._modules)

    def _parseArgs(self):
        import sys
        n=len(sys.argv)-1
        for i in xrange(1,n+1):
            param=sys.argv[i]
            if param.startswith("-"):
                if param=="-c" and i<n:
                    i+=1
                    self._configFile=sys.argv[i]
                elif param=="-o" and i<n-1:
                    i+=1
                    self._options[sys.argv[i]]=sys.argv[i+1]
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
            for arg in self._config.xsd7config[0].args[0].param:
                if not self._args.has_key(arg.pname):
                    self._args[arg.pname] = arg.pvalue
        for arg in self._options_defaults:
            if not self._options.has_key(arg):
                self._options[arg] = self._options_defaults[arg]
        #print self._options

    def _runcmd(self,cmd,args,modules):
        if cmd==None or cmd=="help":
            print """
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
        for m in modules:
            if cmd=="get":
                self._bootStrap.get(m)
            elif cmd=="update":
                self._bootStrap.update(m)
            elif cmd=="remove":
                self._bootStrap.remove(m)
            elif cmd=="patch":
                self._bootStrap.patch(m)
            elif cmd=="clean":
                self._bootStrap.clean(m)
            elif cmd=="install":
                self._bootStrap.install(m)
            elif cmd=="auto":
                self._bootStrap.auto(m)
            else:
                print "Unknown command %s" %(cmd,)


if __name__ == "__main__":
    app = MainApp()

