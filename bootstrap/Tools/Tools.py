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
Some Tools
"""

__version__ = "$Revision$"

__all__ = ["WgetTool","CVSTool","SVNTool","MkdirTool","CdTool"]


import os
import shutil
import time


class ToolNotInstalled(Exception): pass
class ToolError(Exception): pass


class Tool(object):
    
    def check(self):
        pass


class DownloadTool(Tool):

    def get(self,args):
        print args


class WgetTool(DownloadTool):
    
    def check(self):
        if os.system("wget -V")!=0:
            raise ToolNotInstalled, \
            "wget not installed, " \
            "on debian based systems you may install it by apt-get install wget"

    def download(self,what,where):
        if os.system("wget %s -P %s" %(what,where))!=0:
            raise ToolError, "Cannot donwload %s" %(what)
    
    def unpack(self,what,where):
        if what.endswith('.tar.bz2'):
            mode = 'r:bz2'
            pg = 'tar'
        elif what.endswith('.tar.gz'):
            mode = 'r:gz'
            pg = 'tar'
        else:
            raise ToolError,"Unrecognized packaging format %s" %(what,)
        
        if pg == 'tar':
            import tarfile
            t = tarfile.open(what,mode)
            #t.extractall(where)
            ns = len(t.getnames())
            ii = 0
            tt1 = time.time()-1
            tt2 = time.time()
            for f in t:
                if tt2-tt1 >= .5:
                    print "\b\rExtracting %s %i%%" %(what,100*ii/ns),
                    import sys
                    sys.stdout.flush()
                    tt1 = tt2
                #print tt1, tt2
                tt2 = time.time()
                ii = ii+1
                #print f.name
                if f.isdir():
                    f.mode=0755
                t.extract(f,where)
                #print os.path.dirname(where + '/' + f.name)
                os.chmod(os.path.dirname(where + '/' + f.name),0755)
            t.close()
            print "\b\rExtracting %s done!" %(what)

    def md5(self,filen):
        import md5
        m = md5.new()
        f = file(filen,'rb')
        piece = f.read(4096)
        while len(piece!=0):
            m.update(piece)
        return m.hexdigest()
        f.close()

    def get(self,args):
        self.check()
        downloads = args['downloads']
        output = args['output']
        addr = args['addr']
        fname = os.path.basename(addr)
        file = downloads + '/' + fname
        path = output + '/' + args['path']
        if os.path.exists(file) and not args['redownload']:
            print "%s already exists, skipping..." %(fname,)
        else:
            self.download(addr,downloads)
        md5 = self.md5(file)
        print "MD5 %s" %(md5,)
        if args.has_key('md5'):
            if md5!=args['md5']:
                raise ToolError, "Checksum missmatch, source package may have been altered!"

        if os.path.exists(path) and not args['update'] and not args['redownload']:
            print "%s already unpacked, skipping..." %(path,)
        else:
            if os.path.exists(path):
                print "Removing old version..."
                shutil.rmtree(path)

            self.unpack(file,output)
        
            if args.has_key('renamefrom'):
                renpath = output + '/' + args['renamefrom']
                os.rename(renpath,path)


class CVSTool(DownloadTool):
    
    def check(self):
        if os.system("cvs -v")!=0:
            raise ToolNotInstalled, \
            "cvs not installed, " \
            "on debian based systems you may install it by apt-get install cvs"

    def get(self,args):
        self.check()
        output = args['output']
        addr = args['addr']
        path = output + '/' + args['path']
        module = args['module']

        cdir = os.getcwd()
        try:
            os.chdir(output)
            if os.path.exists(path) and not args['redownload']:
                print "%s already exists, skipping..." %(path)
                if args['update']:
                    os.chdir(args['path'])
                    if os.system("cvs -z9 update")!=0:
                        raise ToolError                
            else:
                if os.path.exists(path):
                    shutil.rmtree(path)
                if os.system("cvs -z9 -d %s co %s" %(addr,module))!=0:
                    raise ToolError
                if args.has_key('renamefrom'):
                    renpath = output + '/' + args['renamefrom']
                    os.rename(renpath,path)
        except ToolError,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)


class SVNTool(DownloadTool):
    
    def check(self):
        if os.system("svn --version")!=0:
            raise ToolNotInstalled, \
            "svn not installed, " \
            "on debian based systems you may install it by apt-get install svn"

    def get(self,args):
        self.check()
        output = args['output']
        addr = args['addr']
        path = output + '/' + args['path']

        cdir = os.getcwd()
        try:
            os.chdir(output)
            if os.path.exists(path) and not args['redownload']:
                print "%s already exists, skipping..." %(path)
                if args['update']:
                    os.chdir(args['path'])
                    if os.system("svn update")!=0:
                        raise ToolError                
            else:
                if os.path.exists(path):
                    shutil.rmtree(path)
                if os.system("svn co %s" %(addr))!=0:
                    raise ToolError
                if args.has_key('renamefrom'):
                    renpath = output + '/' + args['renamefrom']
                    os.rename(renpath,path)
        except ToolError,e:
            os.chdir(cdir)
            raise e
        os.chdir(cdir)


class MkdirTool(Tool):

    def run(self,args):
        #print args
        if not os.path.exists(args['path']):
            os.mkdir(args['path'],0755)


class CdTool(Tool):
    
    def run(self,args):
        os.chdir(args['path'])

