#!/bin/bash
# $Id$

SCRIPT_LOCATION=`dirname $0`
cd $SCRIPT_LOCATION/../
export PREFIX=`pwd`/runtime
#echo $SCRIPT_LOCATION
echo "sd7 Maintenance shell"

export PATH=$PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$PREFIX/lib
export CPPFLAGS=-I$PREFIX/include
export LDFLAGS=-L$PREFIX/lib
export PKG_CONFIG_PATH=$PREFIX/lib/pkgconfig
#export LD_PRELOAD=$LD_LIBRARY_PATH/libCEGUIBase.so

PYSHELL="
import sys
version = sys.version_info
print \"%s.%s\" % (version[0], version[1])
"
PYTHONVERSION=`python -c "$PYSHELL"`
echo "Using python $PYTHONVERSION"


export PYTHONPATH=`pwd`:$PREFIX/lib/python$PYTHONVERSION/site-packages

if [ $# -eq 0 ]; then
  bash
else
  $@
fi

