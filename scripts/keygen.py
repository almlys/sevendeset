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

__all__ = []

import re

def gen():

    head = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    sd7 Project Engine
#    Copyright (C) 2008 Alberto Montañola Lacort
#    Licensed under the GNU GPL. For full terms see the file COPYING.
#
#    Id: $Id$
#
# NOTICE THIS FILE HAS BEEN AUTOMATICALLY GENERATED FROM OISKeys.h
#  BY USING scripts/keygen.py
#
# ALL CHANGES WILL BE LOST!

__version__ = "$Revision$"

__all__ = ["Key"]

"""
    
    keytable = {}
    sortedkeys = []

    replace = {
        "ESCAPE" : "ESC",
        "LCONTROL" : "LCTRL",
        "RCONTROL" : "RCTRL",
        "LMENU" : "LALT",
        "RMENU" : "RALT",
        "SYSRQ" : "PRTSC",
    }

    f = file("depends/ois/includes/OISKeyboard.h")
    for l in f.readlines():
        #print l,
        res = re.search('KC_([a-zA-Z0-9-_]*).*=.*(0x[0-9A-Fa-f]{2})',l)
        if res != None:
            #print res.group(1), res.group(2)
            name, val = res.group(1), int(res.group(2),16)
            if name in replace.keys():
                name = replace[name]
            keytable[name] = val
            sortedkeys.append(name)
    f.close()

    buf = head
    buf +="""
    
class Key(object):

"""
    buf2 = """
    name2keyid = {
"""

    buf3 = """    }

    keyid2name = {
"""

    for key in sortedkeys:
        #print "%s : 0x%02X" %(key, keytable[key])
        if key in ("0","1","2","3","4","5","6","7","8","9"):
            buf+= "    N%s = %i\n" %(key, keytable[key])
            buf2+= "        '%s' : %i,\n" %(key,keytable[key])
            buf2+= "        'N%s' : %i,\n" %(key,keytable[key])
            buf3+= "        %i : 'N%s',\n" %(keytable[key],key)
        else:
            buf+= "    %s = %i\n" %(key, keytable[key])
            buf2+= "        '%s' : %i,\n" %(key,keytable[key])
            buf3+= "        %i : '%s',\n" %(keytable[key],key)

    buf += buf2
    buf += buf3
    buf +="""    }

    @staticmethod
    def toString(id):
        return Key.keyid2name[id]

    @staticmethod
    def toKeyId(name):
        return Key.name2keyid[name]
    
    """

    #print buf
    f = file("sd7/engine/input/OISKeys.py","w")
    f.write(buf)
    f.close()


if __name__ == "__main__":

    gen()
