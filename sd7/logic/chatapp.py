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

__all__ = ["ChatApp"]

from sd7.engine.controller import Controller
from sd7.engine import Engine

import random

class TestCrash(Exception): pass

class ChatApp(Controller):

    _history = []
    _maxlines = 20
    _retardedmsg = []
    _time = 0
    _wtime = random.uniform(1.8,6.2)
    
    def __init__(self,params):
        Controller.__init__(self,params,"console")
        self._visible = True

    def initialize(self):
        Controller.initialize(self)

        # get the GUI and load the chat View
        self._gui = Engine().getGUI()
        self._gui.loadView("chat.layout")
        # Watch for input events
        self._gui.subscribeEvent("Chat/ChatWindow/ChatOkBtn",
            "PushButton/EventClicked", self.onInput)
        self._gui.subscribeEvent("Chat/ChatWindow/ChatInput",
            "Editbox/EventTextAccepted", self.onInput)
        self._gui.subscribeEvent("Chat/ChatWindow/ChatInput",
            "Editbox/EventActivated", self.onFocus)
    
        self._textBox = self._gui.getObject("Chat/ChatWindow/ChatInput")
        self._chatBox = self._gui.getObject("Chat/ChatWindow/ChatBox")
        #.setText("Connection code is missing")
    
        # get Net and watch for incomming messages
        #self._net = wathever
        #self._net.subscribeMsg("chat,",self.onMsg)
        self.setVisible(False)

    def terminate(self):
        self._gui.destroyObject("Chat/ChatWindow")
        Controller.terminate(self)

    def setVisible(self,vis = None):
        if vis is not None:
            self._visible = vis
        else:
            self._visible = not self._visible
        self._gui.getObject("Chat/ChatWindow").setVisible(self._visible)
        if self._visible:
            bi = Engine().getHookMGR().findController("basicInput")
            if bi:
                bi.toggleGUIFocus(self._visible)
            self._textBox.activate()

    def onFocus(self,e):
        self._textBox.setText("")

    def processCommand(self,cmd):
        try:
            args = cmd.split()
            cmd = args.pop(0).lower()
            if cmd.lower() in ("quit","exit","logout","killme"):
                Engine().terminate()
            elif cmd == "hsize" and len(args)>0:
                self._maxlines = int(args[0])
            elif cmd == "help":
                if len(args) > 0:
                    ht = args[0]
                    if ht.lower() in ("quit","exit","logout","killme"):
                        self.addMsg("Does what the command says")
                        self.addRetardedMsg("HAL: Dave, perhaphs you should think about it...")
                        self.addRetardedMsg("HAL: Dave, what are you doing?")
                    elif ht.lower() == "hsize":
                        self.addMsg("Sets the history size")
                    else:
                        self.addMsg("Unknwon help topic %s",ht)
                else:
                    self.addMsg("Avaliable commands are:")
                    self.addMsg("quit, hsize")
                    self.addMsg("Type help command for more information")
            elif cmd == "clear":
                self.clear()
            elif cmd == "list":
                ll = Engine().getHookMGR().list()
                map = { False: { True : "Running", False : "Stopped"},
                        True : { True: "Running*", False : "Stopped*"}}
                for l in ll.keys():
                    a, b = ll[l]
                    self.addMsg("%s - %s" %(l,map[a][b]))

            elif cmd == "start" and len(args)>0:
                Engine().getHookMGR().start(args[0])
                self.addMsg("%s started..." %(args[0]))
            elif cmd == "stop" and len(args)>0:
                Engine().getHookMGR().stop(args[0])
                try:
                    self.addMsg("%s stopped..." %(args[0]))
                except:
                    pass
            elif cmd == "restart" and len(args)>0:
                Engine().getHookMGR().restart(args[0])
                try:
                    self.addMsg("%s restarted..." %(args[0]))
                except:
                    pass
            elif cmd == "bind" and len(args)>1:
                Engine().getHookMGR().bind(args[0],args[1])
            elif cmd == "crash":
                raise TestCrash,"Crashing requested by user"
            else:
                self.addMsg("I'm sorry, I'm afraid I can't do that")
                self.addRetardedMsg("yet!")
        except TestCrash,e:
            raise e
        except Exception,e:
            self.addMsg("Exception: %s" %(e,))
            self.addRetardedMsg("System: Perhaps you should think about something different")


    def clear(self):
        self._history = []
        self._chatBox.setText("")

    def onInput(self,e):
        msg = self._textBox.getText()
        self._textBox.setText("")
        msg = str(msg).strip()
        if len(msg) == 0:
            return
        elif msg.startswith("/"):
            self.processCommand(msg[1:])
        else:
            self.addMsg("You: %s" %(msg))
        if msg.lower() in ("hello", "hi", "howa", "hau", "hei", "hola", "ole"):
            ms = ["Hello there", "Hi, how is going?", "Hey there!",
                    "Welcome to the sd7 Engine demo", "Welcome",
                    "Bienvenido", "Benvingut", "Sayonara", "Bon Giorno",
                    "Bon dia","Bones!","HELLO!","HOYGAN!! HAY ALGUIEN ALLI?"]
            self.addRetardedMsg("Someone: %s" %(ms[int(random.uniform(0,len(ms)))]))

    def addMsg(self, msg):
        self._history.append(msg)
        if len(self._history) > self._maxlines:
            self._history.pop(0)
        txt = "\n".join(self._history)
        self._chatBox.setText(txt)
        print "%s" %(msg,)
        self._chatBox.setCaratIndex(len(txt))

    def addRetardedMsg(self,msg):
        self._retardedmsg.append(msg)

    def onAction(self, name, down):
        if down:
            if name == "console":
                self.setVisible()
                return True
                
    def onFrame(self,evt):
        time = evt.timeSinceLastFrame
        self._time += time

        if self._time > self._wtime:
            self._time = 0
            self._wtime = random.uniform(1.8,6.2)
            if len(self._retardedmsg)!=0:
                self.addMsg(self._retardedmsg.pop(0))


    