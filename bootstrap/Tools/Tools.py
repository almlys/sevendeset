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

__all__ = ["WgetTool","WgetTool2","CVSTool","SVNTool","MkdirTool","CdTool"]

import sys
import os
import shutil
import time


class ToolNotInstalled(Exception): pass
class ToolError(Exception): pass
class ChecksumError(Exception): pass


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
        # Oye, esto rompe todo lo que hemos aprendido durante estos
        # ultimos años, con lo bonito que quedaria usar una Factoria
        # y registrar en ella los tipos soportados (huh)
        if what.endswith('.tar.bz2'):
            mode = 'r:bz2'
            pg = 'tar'
        elif what.endswith('.tar.gz'):
            mode = 'r:gz'
            pg = 'tar'
        elif what.endswith('.zip'):
            pg = 'zip'
        else:
            raise ToolError,"Unrecognized packaging format %s" %(what,)
        
        if pg == 'tar':
            import tarfile
            print "\rExtracting %s %i%%" %(what,0),
            t = tarfile.open(what,mode)
            #t.extractall(where)
            ns = len(t.getnames())
            ii = 0
            tt1 = time.time()-1
            tt2 = time.time()
            for f in t:
                if tt2-tt1 >= .5:
                    print "\rExtracting %s %i%%" %(what,100*ii/ns),
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
            print "\rExtracting %s done!" %(what)
        elif pg == 'zip':
            import zipfile
            print "\rExtracting %s %i%%" %(what,0),
            t = zipfile.ZipFile(what,'r')
            ns = len(t.namelist())
            ii = 0
            tt1 = time.time()-1
            tt2 = time.time()
            for f in t.namelist():
                if tt2-tt1 >= .5:
                    print "\rExtracting %s %i%%" %(what,100*ii/ns),
                    sys.stdout.flush()
                    tt1 = tt2
                #print tt1, tt2
                tt2 = time.time()
                ii = ii+1
                
                #print f
                base_dir = where + '/' + os.path.dirname(f)
                if not os.path.exists(base_dir):
                    os.makedirs(base_dir,0755)
                if os.path.basename(f) == "":
                    continue
                foam = file(where + '/' + f,'wb')
                foam.write(t.read(f))
                foam.close()
            t.close()
            print "\rExtracting %s done!" %(what)


    def md5(self,filen):
        import md5
        m = md5.new()
        f = file(filen,'rb')
        piece = f.read(4096)
        while len(piece)!=0:
            m.update(piece)
            piece = f.read(4096)
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
                raise ChecksumError, "Checksum missmatch, source package may have been altered!"

        if os.path.exists(path) and not args['update'] and not args['redownload']:
            print "%s already unpacked, skipping..." %(path,)
        else:
            if os.path.exists(path):
                print "Removing old version..."
                shutil.rmtree(path)

            print "I'm going to unpack %s" %(file,)
            self.unpack(file,output)
        
            if args.has_key('renamefrom'):
                renpath = output + '/' + args['renamefrom']
                os.rename(renpath,path)


class WgetTool2(WgetTool):
    
    def check(self):
        pass
    
    def download(self,what,where):
        try:
            import urllib2
            opener = urllib2.build_opener()
            #opener.addheaders = [('User-Agent', 'sd7/BootStrap (see http://7d7.almlys.org/BootStrap)')]
            f = opener.open(what)
            print "Opening %s" %(f.geturl())
            headers = f.info()
            if headers.has_key('Content-Length'):
                size = int(headers['Content-Length'])
            else:
                size = 0
            bsize = 4098
            mfname = os.path.basename(f.geturl())
            fout = file(where + '/' + mfname,'wb')
            tsize = 0
            pchars = "|/-\\"
            i = 0

            tt1 = time.time()
            tt2 = time.time()
            
            achunk = 0
            pchunk = 0
            timer = .5

            while True:
                input = f.read(bsize)
                fout.write(input)
                sbsize = len(input)
                tsize += sbsize
                pchunk += sbsize
                if (size == 0 and len(input) == 0):
                    break
                if tsize >= size:
                    break
                if len(input) == 0:
                    continue
                # This is getting dirty

                if tt2-tt1 >= timer:
                    if achunk == 0:
                        achunk = pchunk
                    else:
                        achunk = (achunk + pchunk) / 2
                    pchunk = 0

                    if size!=0:
                        print "\rDownloading %s %i%% %s %i KBps [%i/%iKB]" \
                        %(mfname, (tsize * 100 / size), pchars[i],
                         (achunk/timer)/1024, tsize/1024, size/1024),
                    else:
                        print "\rDownloading %s %s %i KBps [%iKB]" \
                        %(mfname, pchars[i], (achunk/timer)/1024, tsize/1024),
                    sys.stdout.flush()
                    tt1 = tt2
                    i += 1
                    if i >= len(pchars):
                        i = 0
                tt2 = time.time()
            fout.close()
            f.close()
            print "\rDownloading %s done!                                   " %(what,)
        #except urllib2.HTTPError,e:
        except Exception,e:
            raise ToolError,e




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
        if args.has_key('revision'):
            revision = args['revision']
            extra = " -D %s " %(revision,)
        else:
            revision = None
            extra = ""

        cdir = os.getcwd()
        try:
            os.chdir(output)
            if os.path.exists(path) and not args['redownload']:
                print "%s already exists, skipping..." %(path)
                if args['update']:
                    os.chdir(args['path'])
                    if os.system("cvs -z9 update%s" %(extra,))!=0:
                        raise ToolError                
            else:
                if os.path.exists(path):
                    shutil.rmtree(path)
                if os.system("cvs -z9 -d %s co%s %s" %(addr,extra,module))!=0:
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

        if args.has_key('revision'):
            revision = args['revision']
            extra = " -r %s " %(revision,)
        else:
            revision = None
            extra = ""

        cdir = os.getcwd()
        try:
            os.chdir(output)
            if os.path.exists(path) and not args['redownload']:
                print "%s already exists, skipping..." %(path)
                if args['update']:
                    os.chdir(args['path'])
                    if os.system("svn%s update" %(extra,))!=0:
                        raise ToolError                
            else:
                if os.path.exists(path):
                    shutil.rmtree(path)
                if os.system("svn%s co %s" %(extra,addr))!=0:
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
        path = args['path']
        import re
        while True:
            result = re.search("\$\{([a-zA-Z_]+)\}", path)
            if result == None:
                break
            keyword = result.group(1)
            match = result.group()
            if os.environ.has_key(keyword):
                value = os.environ[keyword]
            else:
                print "Warning: Undefined keyword %s" %(keyword,)
                value = ""
            path = path.replace(match,value)
        path = path.replace('\\$','$').replace('\\{','{').replace('\\}','}')
        os.chdir(path)

