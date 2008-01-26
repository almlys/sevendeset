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
XML Parsing help tools
"""

__version__ = "$Revision$"

__all__ = ["XMLParser",]


import xml.parsers.expat as xmlp


class pnode(object):
    """
    Implements a node from the XML tree
    Attributes of the node are accessed appending "p" to the member name.
    Elements of the tree are accessed appending "x" to the member name.
    
        <test>
            <name val="hi" />
        </test>
        
        val = xml_parser.xtest[0].xname[0].pname
    
    """

    def __init__(self,name,attrs):
        self.name=name
        self.attrs=attrs
        self.data=""

    def __getattribute__(self,name):
#        if name.startswith("_"):
#            return object.__getattribute__(self,name[1:])
#        else:
#            if name in self.attrs:
#                return self.attrs[name]
#            else:
#                raise AttributeError,name
#        if name.startswith("x"):
#            attr=object.__getattribute__(self,name)
#            if len(attr)==1:
#                return attr[0]
#            else:
#                return attr
        if name.startswith("p"):
            if name[1:] in self.attrs:
                return self.attrs[name[1:]]
            else:
                raise AttributeError,name
        else:
            return object.__getattribute__(self,name)


class XMLParser(object):
    """
    XML Parser help class
    
    """
    
    def __init__(self):
        self.stack=[]
        self.current=None

    def _start_element(self,name,attrs):
        #print "Start element:", name, attrs
        if self.current==None:
            self.current=self
        node=pnode(name,attrs)
        try:
            var=getattr(self.current,"x" + name)
            var.append(node)
        except AttributeError:
            setattr(self.current,"x" + name.lower(),[node,])
        self.current=node
        self.stack.append(node)            

    def _end_element(self,name):
        #print "End element", name
        if self.current!=None:
            self.stack.remove(self.current)
            if len(self.stack)>0:
                self.current=self.stack[len(self.stack)-1]
            else:
                self.current=None

    def _char_data(self,data):
        #print "Character data:", repr(data), str(data)
        self.current.data = self.current.data + str(data)

    def parse(self,input):
        """
        Parses a string
        @param input: Input string to parse
        """
        p = xmlp.ParserCreate()

        p.StartElementHandler = self._start_element
        p.EndElementHandler = self._end_element
        p.CharacterDataHandler = self._char_data

        p.Parse(input,1)

    def readfile(self,inn):
        """
        Reads and parses a file
        @param inn: Name of the file to parse
        """
        f = file(inn,"r")
        self.parse(f.read())
        f.close()


if __name__ == "__main__":
    a=XMLParser()
    a.parse("""<worksheet name="Easy-#1-(37)-[08/01/2007]">
        <cell value="7" idx="0"></cell>
        <cell value="8" idx="1"></cell>
        <cell value="0" idx="2"></cell>
        </worksheet>""")
    #print a.xworksheet[0].pnames
    assert(a.xworksheet[0].pname=="Easy-#1-(37)-[08/01/2007]")
    for i,cell in enumerate(a.xworksheet[0].xcell):
        assert(int(cell.pidx)==i)
        if i==0:
            assert(int(cell.pvalue)==7)
        elif i==1:
            assert(int(cell.pvalue)==8)
        else:
            assert(int(cell.pvalue)==0)
