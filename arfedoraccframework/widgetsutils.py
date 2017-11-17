#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  Copyright 2017 youcefsourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import time
import subprocess
import threading

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent):
        Gtk.MessageDialog.__init__(self,parent=parent,flags=Gtk.DialogFlags.MODAL,type=Gtk.MessageType.QUESTION,buttons=Gtk.ButtonsType.OK_CANCEL,message_format=msg)
        
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            return True
        else:
            self.destroy()
            return False


class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message)
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def start(self):
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()
        return False


class RunAndWriteToTextView(threading.Thread):
    def __init__(self,parent,sensitive,commands,textview,end,spinner,timeout=0,commandtimeout=0):
        threading.Thread.__init__(self)
        self.parent          = parent
        self.sensitive       = sensitive
        self.commands        = commands
        self.timeout         = timeout
        self.commandtimeout  = commandtimeout
        self.end             = end
        self.textview        = textview
        self.spinner         = spinner
        self.textviewbuffer  = self.textview.get_buffer()
        
    def run(self):
        if self.sensitive:
            GLib.idle_add(self.parent.set_sensitive,False)
        if self.spinner!=None:
            GLib.idle_add(self.spinner.start)
            GLib.idle_add(self.spinner.show)
        for command in self.commands:
            if command[1]=="free":
                out = subprocess.Popen(command[0],shell=command[2],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                while out.poll()==None:
                    line = out.stdout.readline().decode("utf-8").strip()
                    if line:
                        GLib.idle_add(self.textviewbuffer.insert_at_cursor,line+"\n",len(line)+1)
                    time.sleep(self.timeout)
                if  out.poll()!=0:
                    GLib.idle_add(self.textviewbuffer.insert_at_cursor,self.end,len(self.end))
                    if self.sensitive:
                        GLib.idle_add(self.parent.set_sensitive,True)
                    if self.spinner!=None:
                        GLib.idle_add(self.spinner.hide)
                        GLib.idle_add(self.spinner.stop)
                    return
            else:
                out = subprocess.Popen(command[0],shell=command[2],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
                out = out.decode("utf-8")
                GLib.idle_add(self.textviewbuffer.insert_at_cursor,out,len(out))
                

            time.sleep(self.commandtimeout)
            GLib.idle_add(self.textviewbuffer.insert_at_cursor,self.end,len(self.end))
            
        if self.sensitive:
            GLib.idle_add(self.parent.set_sensitive,True)
        if self.spinner!=None:
            GLib.idle_add(self.spinner.hide)
            GLib.idle_add(self.spinner.stop)


class RunTextView(Gtk.ScrolledWindow):
    def __init__(self,parent,sensitive,commands=None,timeout=0,commandtimeout=0,end="\n\n",\
                 editable=False,cursor_visible=False,justification=Gtk.Justification.LEFT,wrap_mode=Gtk.WrapMode.CHAR,\
                 spinner=None):
        Gtk.ScrolledWindow.__init__(self)
        self.parent          = parent
        self.sensitive       = sensitive
        self.commands        = commands
        self.timeout         = timeout
        self.commandtimeout  = commandtimeout
        self.end             = end
        self.editable        = editable
        self.cursor_visible  = cursor_visible
        self.justification   = justification
        self.wrap_mode       = wrap_mode
        self.spinner         = spinner
        
        self.t = Gtk.TextView(editable=self.editable,cursor_visible=self.cursor_visible,justification=self.justification,\
        wrap_mode=self.wrap_mode)
        
        self.add_with_viewport(self.t)
        self.t.connect("size-allocate", self._autoscroll)


    def start(self):
        t = RunAndWriteToTextView(self.parent,self.sensitive,self.commands,self.t,self.end,self.spinner,self.timeout)
        t.start()
        
    def _autoscroll(self,widget,rec):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())
        

class TooltipWindow(Gtk.Window):
    def __init__(self,image):
        Gtk.Window.__init__(self)
        self.image = image
        self.add(self.image)
        self.show_all()
