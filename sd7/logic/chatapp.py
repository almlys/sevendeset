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


class Commands(object):

    _help = { "quit" : "Does what the command says",
              "hsize" : "Sets the history size: hsize size",
              "clear" : "Clears the console",
              "list" : "List running processes",
              "start" : "Starts up a process",
              "stop" : "Stops a process",
              "restart" : "Restarts a process",
              "bind" : "Binds a process into the HookMGR: bind name path"
              }

    def __init__(self, chatapp):
        self._chatapp = chatapp

    def quit(self):
        Engine().terminate()

    def exit(self):
        self.quit()

    def logout(self):
        self.quit()

    def killme(self):
        self.quit()

    def hsize(self, size):
        self._chatapp._maxlines = int(size)

    def help(self, topic = None):
        if topic is None:
            self._chatapp.addMsg("Avaliable commands are:")
            self._chatapp.addMsg(",".join(self._help.keys()))
            self._chatapp.addMsg("Type help command for more information")
            return
        topic = topic.lower()
        if topic in ("exit", "logout", "killme"):
            topic = "exit"
        if self._help.has_key(topic):
            self._chatapp.addMsg(self._help[topic])
            if topic == "exit":
                self.addRetardedMsg("HAL: Dave, perhaphs you should think about it...")
                self.addRetardedMsg("HAL: Dave, what are you doing?")
        else:
            self._chatapp.addMsg("Unknwon help topic %s" %(topic,))

    def clear(self):
        self._chatapp.clear()

    def list(self):
        procs = Engine().getHookMGR().list()
        map = { False: { True : "Running", False : "Stopped"},
                True : { True: "Running*", False : "Stopped*"}}
        for p in procs.keys():
            autostart, running = procs[p]
            self._chatapp.addMsg("%s - %s" %(p, map[autostart][running]))

    def start(self, name):
        Engine().getHookMGR().start(name)
        self._chatapp.addMsg("%s started..." %(name))

    def stop(self, name):
        Engine().getHookMGR().stop(name)
        try:
            self._chatapp.addMsg("%s stopped..." %(name))
        except:
            pass

    def restart(self, name):
        Engine().getHookMGR().restart(name)
        try:
            self._chatapp.addMsg("%s restarted..." %(name))
        except:
            pass

    def bind(self, name, path):
        Engine().getHookMGR().bind(name, path)

    def crash(self):
        raise TestCrash,"Crashing requested by user"

    def destroyobject(self, name):
        Engine().getWorldMGR().destroyObject(name)



class ChatApp(Controller):

    _history = []
    _maxlines = 20
    _retardedmsg = []
    _time = 0
    _wtime = random.uniform(1.8,6.2)
    
    def __init__(self,params):
        Controller.__init__(self,params,"console")
        self._visible = True
        self._cmds = Commands(self)

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
            if hasattr(self._cmds, cmd):
                getattr(self._cmds, cmd)(*args)
            else:
                self.addMsg("I'm sorry, I'm afraid I can't do that")
                self.addRetardedMsg("yet!")
        except TestCrash:
            raise
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
            elif name == "reload":
                self.addMsg("Reloading world...")
                Engine().getHookMGR().restart("world3")
                return True
                
    def onFrame(self,evt):
        time = evt.timeSinceLastFrame
        self._time += time

        if self._time > self._wtime:
            self._time = 0
            self._wtime = random.uniform(1.8,6.2)
            if len(self._retardedmsg)!=0:
                self.addMsg(self._retardedmsg.pop(0))


    