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

from bootstrap.xmlparser import XMLParser
from sd7.engine.Events import Event
from sd7.engine.Events import EventType
from sd7.engine.input.keys import Key
from sd7.engine.subsystem import SubSystem

__version__ = "$Revision$"

__all__ = ["ActionMapper","ActionMapperException"]


class ActionMapperException(Exception): pass



class Action(object):
    
    def __init__(self,name,target=None,prio=1,invert=False):
        self.name = name
        self.target = target
        self.priority = prio
        self.invert = invert
        self.abs = 0
        self.rel = 0
        self.type = 0

    def __str__(self):
        return str((self.name,self.target,self.priority,self.invert))


class EventDispatcher(object):

    def __init__(self,logfunc=None):
        self._prioConsumers = []
        self._normalConsumers = []
        if logfunc == None:
            self.log = self._log
        else:
            self.log = logfunc

    def _log(self,msg):
        print msg

    def addEventListener(self, listenner, priority=1):
        """ Register a event listener """
        if priority < 1 :
            self._prioConsumers.append(listenner)
        else:
            self._normalConsumers.append(listenner)

    def removeEventListener(self, listenner):
        """ Remove a event listenner """
        if listenner in self._prioConsumers:
            self._prioConsumers.remove(listenner)
        else:
            self._normalConsumers.remove(listenner)

    def dispatchEvent(self,rawEvt,actionEvt=None):
        if actionEvt == None:
            for o in self._prioConsumers:
                if o.processEvent(rawEvt):
                    return True
            for o in self._normalConsumers:
                if o.processEvent(rawEvt):
                    return True
            return False

        if actionEvt.getObject().priority < 1 :
            for o in self._normalConsumers:
                if o.processEvent(actionEvt):
                    return True

        for o in self._prioConsumers:
            if o.processEvent(rawEvt):
                return True

        for o in self._normalConsumers:
            if o.processEvent(actionEvt):
                return True

        for o in self._normalConsumers:
            if o.processEvent(rawEvt):
                return True

        if actionEvt.getType() == EventType.ACTION_DOWN:
            self.log("Unprocessed event: Action: %s, Raw: %s" %(actionEvt, rawEvt))




class ActionMapper(SubSystem):

    _mask = 0
    _mouse_x = 0
    _mouse_y = 0
    _mouse_z = 0

    def __init__(self,options=None):
        SubSystem.__init__(self,"ActionMapper",True,options)
        self._actionMap = {}
        self._eventDispatcher = EventDispatcher(self.log)

    def initialize(self):
        if not SubSystem.initialize(self):
            raise ActionMapperException,"Init error"
        self._readDefinitions()


    def addEventListener(self, listenner, priority=1):
        """ Register a event listener """
        self._eventDispatcher.addEventListener(listenner, priority)

    def removeEventListener(self, listenner):
        """ Remove a event listenner """
        self._eventDispatcher.removeEventListener(listenner)

    def _readDefinitions(self):
        if self._config.has_key("input.actionmap"):
            fname = self._config.get("input.actionmap")
        else:
            fname = "config/input.xml"
        x = XMLParser()
        x.readfile(fname)

        
        for i in x.xsd7input[0].xinput:
            device = i.pdevice#, i.pname, i.ppriority
            target = None
            priority = 1
            if hasattr(i,"ptarget"):
                target = i.ptarget
            if hasattr(i,"ppriority"):
                priority = int(i.ppriority)

            if hasattr(i,"xaction"):
                for act in i.xaction:
                    aname = act.pname
                    ctarget = target
                    cpriority = priority
                    keybut = ""
                    if hasattr(act, "ptarget"):
                        ctarget = act.ptarget
                    if hasattr(act, "ppriority"):
                        cpriority = int(act.ppriority)

                    if device == "keyboard":
                        if hasattr(act, "pkey"):
                            keybut = act.pkey.upper()
                        if hasattr(act, "pmask"):
                            mask = 0
                            for mi in act.pmask.split(","):
                                if mi.lower() == "shift":
                                    mask += 1
                                elif mi.lower() == "ctrl":
                                    mask += 2
                                elif mi.lower() == "alt":
                                    mask += 4
                            if mask!=0:
                                keybut += str(mask)
                    else:
                        if hasattr(act, "pbutton"):
                            keybut = act.pbutton

                    action = Action(aname,ctarget,cpriority)
                    self._addDefinition(device + keybut,action)

            if hasattr(i,"xaxis") and device != "keyboard":
                for axis in i.xaxis:
                    aname = axis.pname
                    ctarget = target
                    cpriority = priority
                    cinvert = False
                    keybut = ""
                    if hasattr(axis,"ptarget"):
                        ctarget = axis.ptarget
                    if hasattr(axis,"ppriority"):
                        cpriority = int(axis.ppriority)
                    if hasattr(axis,"pinvert") and \
                        axis.pinvert.lower().startswith("t"):
                        cinvert =True
                    if hasattr(axis,"pid"):
                        keybut = axis.pid

                    action = Action(aname,ctarget,cpriority,cinvert)
                    self._addDefinition(device + keybut,action)

    def _addDefinition(self,hash,action):
        self._actionMap[hash] = action


    def _updateKeyMask(self,evt):
        key, etype = evt.getObject().key, evt.getType()
        if key in (Key.LSHIFT, Key.RSHIFT):
            if etype == EventType.KEY_PRESSED:
                self._mask |= 1
            else:
                self._mask &= ~1
        elif key in (Key.LCTRL, Key.RCTRL):
            if etype == EventType.KEY_PRESSED:
                self._mask |= 2
            else:
                self._mask &= ~2
        elif key in (Key.LALT, Key.RALT):
            if etype == EventType.KEY_PRESSED:
                self._mask |= 4
            else:
                self._mask &= ~4
        #print self._mask


    def processEvent(self,evt):
        etype = evt.getType()
        if etype in [EventType.KEY_PRESSED, EventType.MOUSE_PRESSED]:
            evtType = EventType.ACTION_DOWN
        elif etype in [EventType.KEY_RELEASED, EventType.MOUSE_RELEASED]:
            evtType = EventType.ACTION_UP
        elif etype in [EventType.MOUSE_MOVED]:
            evtType = EventType.ACTION_AXIS
        else:
            self.log("Unkwnon unprocessed event: %s",str(evt))
            return False

        if etype in [EventType.KEY_PRESSED, EventType.KEY_RELEASED]:
            self._updateKeyMask(evt)
            hash = "keyboard"
            hash += Key.toString(evt.getObject().key)
            if self._mask != 0:
                hash += str(self._mask)
            if self._actionMap.has_key(hash):
                actionEvt = Event(evtType,self._actionMap[hash])
                return self._eventDispatcher.dispatchEvent(evt,actionEvt)
        elif etype in [EventType.MOUSE_PRESSED,
            EventType.MOUSE_RELEASED]:
            hash = "mouse"
            hash += str(evt.getObject().id+1)
            if self._actionMap.has_key(hash):
                actionEvt = Event(evtType,self._actionMap[hash])
                return self._eventDispatcher.dispatchEvent(evt,actionEvt)
        elif etype in [EventType.MOUSE_MOVED]:
            hash = "mouse"
            mo = evt.getObject()
            x,y,z = mo.X.abs, mo.Y.abs, mo.Z.abs
            res = False
            if self._mouse_x != x:
                self._mouse_x = x
                hash += "x"
                if self._actionMap.has_key(hash):
                    acc = self._actionMap[hash]
                    acc.abs = x
                    acc.rel = mo.X.rel
                    actionEvt = Event(evtType, acc)
                    res |= bool(self._eventDispatcher.dispatchEvent(evt,actionEvt))
            if self._mouse_y != y:
                self._mouse_y = y
                hash += "y"
                if self._actionMap.has_key(hash):
                    acc = self._actionMap[hash]
                    acc.abs = y
                    acc.rel = mo.Y.rel
                    actionEvt = Event(evtType, acc)
                    res |= bool(self._eventDispatcher.dispatchEvent(evt,actionEvt))
            if self._mouse_z != z:
                self._mouse_z = z
                hash += "z"
                if self._actionMap.has_key(hash):
                    acc = self._actionMap[hash]
                    acc.abs = z
                    acc.rel = mo.Z.rel
                    actionEvt = Event(evtType, acc)
                    res |= bool(self._eventDispatcher.dispatchEvent(evt,actionEvt))
            return res

        return self._eventDispatcher.dispatchEvent(evt)




if __name__ == "__main__":
    import os
    os.chdir("../../../")

    am = ActionMapper({"input.actionmap":"config/input.xml"})
    am.initialize()



