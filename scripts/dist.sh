#!/bin/bash
# $Id: shell.sh 46 2008-02-01 13:44:10Z Almlys $

SCRIPT_LOCATION=`dirname $0`
cd $SCRIPT_LOCATION/../
export PREFIX=`pwd`/runtime

PYSHELL="
import sys
version = sys.version.split('.')
print \"%s.%s\" % (version[0], version[1])
"
PYTHONVERSION=`python -c "$PYSHELL"`
echo "Using python $PYTHONVERSION"

PYSHELL="
import sys
version = sys.version.split('.')
print \"%s%s\" % (version[0], version[1])
"
PYTHONVERSION_WITHOUTDOTS=`python -c "$PYSHELL"`

export PYTHONPATH=`pwd`:$PREFIX/lib/python$PYTHONVERSION/site-packages

DIST=dist/sd7runtime_`uname -m`_py$PYTHONVERSION_WITHOUTDOTS


mkdir -p $DIST
mkdir -p $DIST/lib
mkdir -p $DIST/lib/OGRE
mkdir -p $DIST/lib/python$PYTHONVERSION/site-packages/ogre/renderer/OGRE
mkdir -p $DIST/lib/python$PYTHONVERSION/site-packages/ogre/io/OIS
mkdir -p $DIST/lib/python$PYTHONVERSION/site-packages/ogre/gui/CEGUI

## Legal stuff, i need to review it still
svn2cl
cp -rvp $PREFIX/README $DIST
cp -rvp $PREFIX/COPYING $DIST
cp -rvp $PREFIX/ChangeLog $DIST
##

cp -rvp $PREFIX/lib/OGRE/*.so $DIST/lib/OGRE
cp -rvp $PREFIX/lib/*.so $DIST/lib
cp -rvp $PREFIX/lib/*.so.* $DIST/lib
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre

cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/renderer/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/renderer
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/renderer/OGRE/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/renderer/OGRE
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/renderer/OGRE/*.so $DIST/lib/python$PYTHONVERSION/site-packages/ogre/renderer/OGRE

cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/io/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/io
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/io/OIS/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/io/OIS
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/io/OIS/*.so $DIST/lib/python$PYTHONVERSION/site-packages/ogre/io/OIS

cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/gui/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/gui
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/gui/CEGUI/*.py $DIST/lib/python$PYTHONVERSION/site-packages/ogre/gui/CEGUI
cp -rvp $PREFIX/lib/python$PYTHONVERSION/site-packages/ogre/gui/CEGUI/*.so $DIST/lib/python$PYTHONVERSION/site-packages/ogre/gui/CEGUI

FILENAMEDATE=`date +%Y%m%d%H%M%S`

FILENAME=$DIST_`uname -n`_$FILENAMEDATE.tar.bz2

tar cfvj $FILENAME $DIST
