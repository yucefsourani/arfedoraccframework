#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  hashlibbin_v2.0.py.py
#  
#  Copyright 2019 youcef sourani <youssef.m.sourani@gmail.com>
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
import hashlib
import threading
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf,GLib,Pango,GObject,Gdk
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location

button_label         = _("Hash Check")
button_image         = "HASH-256.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Check Files Hash")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-utilities" 

class CustomButton(Gtk.Bin):
    __gsignals__ = {
        'xclosed' : (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE,
                            ()),
        'clicked' : (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE,
                            ())
                    }
    def __init__(self,label,size=None,grid=False,delete=True):
        Gtk.Bin.__init__(self)
        __label       = label
        self_size     = size
        self.__grid   = grid
        self.__delete = delete
        css = b"""
        .XBUTTON {
            border-image: none;
            background-image: none;
            background-color: rgba(255, 255, 255, 0);
            border-radius: 30px;

        }
        .XBUTTON:hover {
            background-color: rgba(255, 0, 0, 1);

        }
        .FLOWBOX {
            background-color: rgba(255, 255, 255, 1);

        }
        .BUTTON {
            border-radius: 30px;
        }
        .h1 {
            font-size: 24px;
        }

        .h2 {
            font-weight: 300;
            font-size: 18px;
        }

        .h3 {
            font-size: 11px;
        }

        .h4 {
            color: alpha (@text_color, 0.7);
            font-weight: bold;
            text-shadow: 0 1px @text_shadow_color;
        }

        .h4 {
            padding-bottom: 6px;
            padding-top: 6px;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
        self.eventbox = Gtk.EventBox()
        self.eventbox.set_events(4096)
        self.eventbox.set_events(8192)
        self.overlay  = Gtk.Overlay()
        self.eventbox.add(self.overlay)
        
        if self.__grid:
            _grid = Gtk.Grid()
            _grid.add(self.eventbox)
        
        self.button  = Gtk.Button()
        self.button.connect("clicked",self.__on_button_clicked)
        self.button.get_style_context().add_class("BUTTON")


        
        self.button.props.label = __label
        if self_size:
            self.button.set_size_request(*size)
        self.overlay.add(self.button)
        

        
        if self.__grid:
            self.add(_grid)
        else:
            self.add(self.eventbox)
        if self.__delete:
            self.eventbox.connect("enter-notify-event",self.__on_button_enter)
            self.eventbox.connect("leave-notify-event",self.__on_button_leave)
        self.show_all()


        
    def __on_xbutton_clicked(self,button):
        self.emit("xclosed")
        
    def __on_button_clicked(self,button):
        self.emit("clicked")

    def __on_button_enter(self,eventbox,d):
        self.xbutton = Gtk.Button.new_from_icon_name("window-close",Gtk.IconSize.SMALL_TOOLBAR)
        #self.xbutton.set_name("XBUTTON")
        self.xbutton.get_style_context().add_class("XBUTTON")
        self.xbutton.set_valign(Gtk.Align.START )
        self.xbutton.set_halign(Gtk.Align.END )
        self.xbutton.set_relief(Gtk.ReliefStyle.NONE)
        self.xbutton.connect("clicked",self.__on_xbutton_clicked)
        self.overlay.add_overlay(self.xbutton)
        self.xbutton.show()
        
    def __on_button_leave(self,eventbox,d):
        self.xbutton.destroy()
    
class ThreadCheck(threading.Thread):
    def __init__(self,algorithms,file_location,hbox,result_label,button,algorithms_button):
        threading.Thread.__init__(self)
        self.algorithms         = algorithms
        self.__file_location    = file_location
        self.hbox               = hbox
        self.result_label       = result_label
        self.button             = button
        self.algorithms_button  = algorithms_button
    
    def run(self):
        vbutton = self.button.get_child()
        bpbar   = Gtk.ProgressBar()
        GLib.idle_add(bpbar.set_show_text,True)
        GLib.idle_add(self.button.set_sensitive,False)
        GLib.idle_add(self.algorithms_button.set_sensitive,False)
        GLib.idle_add(vbutton.pack_start,bpbar,True,True,0)
        GLib.idle_add(vbutton.show_all)
        try:
            h       = hashlib.new(self.algorithms)
            size    = os.path.getsize(self.__file_location)
            psize   = 0
            to_read = 1024 * 1024 * 32
            with open(self.__file_location,"rb") as myfile:########## here and shok ale
                while True:
                    chunk = myfile.read(to_read)
                    if not chunk:
                        break
                    count    = int((psize*100)//size)
                    fraction = count/100
                    h.update(chunk)
                    psize   += to_read
                    GLib.idle_add(bpbar.set_fraction,fraction)
                    GLib.idle_add(bpbar.set_text,str(count)+"%")
                    
        except Exception as e:
            print(e)
            GLib.idle_add(self.result_label.set_text,"ERROR")
            GLib.idle_add(self.hbox.emit,"finish")
            GLib.idle_add(vbutton.remove,bpbar)
            GLib.idle_add(vbutton.show_all)
            GLib.idle_add(bpbar.destroy)
            GLib.idle_add(self.button.set_sensitive,True)
            GLib.idle_add(self.algorithms_button.set_sensitive,True)
            return
        if "shake_" in self.algorithms:
            try :
                l = int(self.algorithms.split("_",1)[-1])*4
                GLib.idle_add(self.result_label.set_text,h.hexdigest(l))
            except Exception as e:
                print(e)
                GLib.idle_add(self.result_label.set_text,"ERROR")
                GLib.idle_add(self.hbox.emit,"finish")
                GLib.idle_add(vbutton.remove,bpbar)
                GLib.idle_add(vbutton.show_all)
                GLib.idle_add(bpbar.destroy)
                GLib.idle_add(self.button.set_sensitive,True)
                GLib.idle_add(self.algorithms_button.set_sensitive,True)
                return 
        else:
            GLib.idle_add(self.result_label.set_text,h.hexdigest())
        GLib.idle_add(self.hbox.emit,"finish")
        GLib.idle_add(vbutton.remove,bpbar)
        GLib.idle_add(vbutton.show_all)
        GLib.idle_add(bpbar.destroy)
        GLib.idle_add(self.button.set_sensitive,True)
        if not self.algorithms_button.button.props.label == "md5":
            GLib.idle_add(self.algorithms_button.set_sensitive,True)
        

class ThreadCheckBox(Gtk.HBox):
    __gsignals__ = {
        'finish' : (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE,
                            ())
                    }
                    
    def __init__(self,algorithms,file_location,process_vbox3,algorithms_button):
        Gtk.HBox.__init__(self)
        self.algorithms         = algorithms
        self.__file_location    = file_location
        self.process_vbox3      = process_vbox3
        self.algorithms_button  = algorithms_button
        self.vbox               = Gtk.VBox()
        
        
        self.result_label       = Gtk.Entry()
        self.result_label.props.editable = False
        #self.result_label.props.justify = Gtk.Justification.FILL
        #self.result_label.props.selectable = True
        #self.result_label.props.wrap = True
        #self.result_label.props.wrap_mode = Pango.WrapMode.CHAR
        self.vbox.pack_start(self.result_label,True,True,0)
        
        self.button             = Gtk.Button()
        vbutton                 = Gtk.VBox()
        blabel                  = Gtk.Label()
        blabel.props.label      = "Start"
        self.button.add(vbutton)
        vbutton.pack_start(blabel,True,True,0)
        self.button.connect("clicked",self.__run)
        
        
        self.pack_start(self.vbox,True,True,0)
        self.process_vbox3.pack_start(self.button,True,True,0)
        self.show_all()
    
    def __run(self,button):
        self.result_label.set_text("")
        if not self.__file_location[0] or not os.path.isfile(self.__file_location[0]):
            return
        ThreadCheck(self.algorithms,self.__file_location[0],self,self.result_label,button,self.algorithms_button).start()

        
        
    
    
class HashLibBin(Gtk.Bin):
    def __init__(self,parent):
        Gtk.Bin.__init__(self)
        self.parent = parent 
        
        self.__file_name = [""]

        self.main_vbox     = Gtk.VBox()
        self.process_vbox1 = Gtk.VBox()
        self.process_vbox2 = Gtk.VBox()
        self.process_vbox3 = Gtk.VBox()
        
        self.process_vbox1.set_homogeneous(True)
        self.process_vbox2.set_homogeneous(True)
        self.process_vbox3.set_homogeneous(True)
        
        
        self.main_vbox.props.spacing = 10
        self.available_algorithms()
        

        self.add(self.main_vbox)

    def available_algorithms(self):
        self.search_entry = Gtk.SearchEntry()
        
        available_grid         = Gtk.Grid()
        self.available_flowbox = Gtk.FlowBox()
        self.available_flowbox.set_filter_func(self.__filter_func)
        
        self.available_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.available_flowbox.get_style_context().add_class("FLOWBOX")
        self.available_flowbox.set_max_children_per_line(50)
        self.available_flowbox.set_homogeneous(True)
        available_grid.add(self.available_flowbox)
        for algorithms in hashlib.algorithms_available:
            if algorithms=="md5":
                continue
            button = CustomButton(algorithms,delete=False)
            button.connect("clicked",self.on_available_algorithms_button_clicked,algorithms,0)
            self.available_flowbox.add(button)
        
        self.current_search_entry = Gtk.SearchEntry()
        current_grid              = Gtk.Grid()
        self.current_flowbox      = Gtk.FlowBox()
        self.current_flowbox.set_filter_func(self.__current_filter_func)
        self.current_flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.current_flowbox.get_style_context().add_class("FLOWBOX")
        self.current_flowbox.set_max_children_per_line(50)
        self.current_flowbox.set_homogeneous(True)
        current_grid.add(self.current_flowbox)
        button = CustomButton("md5")
        self.current_flowbox.add(button)
        self.on_selectd_algorithms(button)
        button.set_sensitive(False)
        
        vseparator1 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        vseparator2 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        
        l1             = Gtk.Label()
        l2             = Gtk.Label()
        l1.props.label = "Available Algorithms"
        l2.props.label = "Selected Algorithms"
        l1.get_style_context().add_class("h1")
        l2.get_style_context().add_class("h1")
        
        self.main_hbox       = Gtk.HBox()

        boxchoose_button     = Gtk.HBox()
        boxchoose_button.props.spacing = 10
        choose_button        = Gtk.Button()
        choose_button.props.label = "Choose File"
        choose_button.connect("clicked", self.on_choose_button_clicked)
        
        
        self.file_name_entry = Gtk.Entry()
        self.file_name_entry_handler = self.file_name_entry.connect("notify::text",self.on_text_changed)
        boxchoose_button.pack_start(choose_button,False,False,0)
        boxchoose_button.pack_start(self.file_name_entry,True,True,0)
        vseparator3 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)

        
        self.main_vbox.pack_start(l1,False,False,0)
        self.main_vbox.pack_start(self.search_entry,False,False,0)
        self.main_vbox.pack_start(available_grid,False,False,0)
        self.main_vbox.pack_start(vseparator1,False,False,0)
        self.main_vbox.pack_start(l2,False,False,0)
        self.main_vbox.pack_start(self.current_search_entry,False,False,0)
        self.main_vbox.pack_start(current_grid,False,False,0)
        self.main_vbox.pack_start(vseparator2,False,False,0)
        self.main_vbox.pack_start(boxchoose_button,False,False,0)
        self.main_vbox.pack_start(vseparator3,False,False,0)
        self.main_vbox.pack_start(self.main_hbox,False,False,0)

        self.main_hbox.props.spacing = 10
        self.main_hbox.pack_start(self.process_vbox1,True,True,0)
        self.main_hbox.pack_start(self.process_vbox2,True,True,0)
        self.main_hbox.pack_start(self.process_vbox3,True,True,0)
        self.search_entry.connect("notify::text",self.available_flowbox_filter)
        self.current_search_entry.connect("notify::text",self.current_flowbox_filter)


        

    def on_available_algorithms_button_clicked(self,button,algorithms,pos=None):
        
        flowboxchild_index = button.get_parent().get_index()
        button.get_parent().destroy()
        button = CustomButton(algorithms)
        
        self.current_flowbox.insert(button,pos)

        algorithms = button.button.props.label
        b = ThreadCheckBox(algorithms,self.__file_name,self.process_vbox3,button)
        l = Gtk.Label()
        l.get_style_context().add_class("h2")
        l.props.label = algorithms
        self.process_vbox1.pack_start(l,True,True,0)
        self.process_vbox2.pack_start(b,True,True,0)

        button.connect("xclosed",self.on_xclosed_clicked,algorithms,flowboxchild_index,b,l)

        self.show_all()
            
    def on_xclosed_clicked(self,button,algorithms,pos,threadbox,label):
        flowboxchild_index = button.get_parent().get_index()
        button.get_parent().destroy()
        button = CustomButton(algorithms,delete=False)
        button.connect("clicked",self.on_available_algorithms_button_clicked,algorithms,flowboxchild_index)
        self.available_flowbox.insert(button,pos)
        self.on_remove_algorithms(button)
        
        self.process_vbox1.remove(label)
        self.process_vbox2.remove(threadbox)
        self.process_vbox3.remove(threadbox.button)
        label.destroy()
        threadbox.button.destroy()
        threadbox.destroy()
        
        self.show_all()
        
    def on_selectd_algorithms(self,button):
        algorithms = button.button.props.label
        b = ThreadCheckBox(algorithms,self.__file_name,self.process_vbox3,button)
        l = Gtk.Label()
        l.get_style_context().add_class("h2")
        l.props.label = algorithms
        self.process_vbox1.pack_start(l,True,True,0)
        self.process_vbox2.pack_start(b,True,True,0)

    
    def on_remove_algorithms(self,button):
        print(button.button.props.label)
        
    def on_choose_button_clicked(self,button):
        dialog = Gtk.FileChooserDialog("Please choose a file", self.parent,
            Gtk.FileChooserAction.OPEN)
        

        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.__file_name[0] = dialog.get_filename()
            with self.file_name_entry.handler_block(self.file_name_entry_handler):
                self.file_name_entry.props.text = dialog.get_filename()
        dialog.destroy()
        
    def on_text_changed(self,entry,text):
        self.__file_name[0] = entry.props.text

    def __filter_func(self,child, *user_data):
        text = self.search_entry.get_text()        
        if not text:
            return True
        else:
            if text in child.get_child().button.props.label:
                return True
            else:
                return False
                
    def __current_filter_func(self,child, *user_data):
        text = self.current_search_entry.get_text()        
        if not text:
            return True
        else:
            if text in child.get_child().button.props.label:
                return True
            else:
                return False
                
    def available_flowbox_filter(self,searchentry,text):
        self.available_flowbox.invalidate_filter()
        
    def current_flowbox_filter(self,searchentry,text):
        self.current_flowbox.invalidate_filter()
        
        

class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.__parent = parent

        mainvbox = Gtk.VBox(spacing=20)
        mainvbox.set_margin_left(60)
        mainvbox.set_margin_right(60)
        vbox1 = Gtk.VBox(spacing=20)
        vbox2 = Gtk.VBox(spacing=20)
        
        self._mainbox_.set_border_width(10)
        self._mainbox_.set_spacing(30)
        
        headerbox    = Gtk.VBox(spacing=6)
        headerlabel  = Gtk.Label()
        headerlabel.props.label      = _("<b>Hash Check</b>")
        headerlabel.props.use_markup = True
        headerlabel.get_style_context().add_class("h1")
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()


        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        
        
        h = HashLibBin(self.__parent)
        mainvbox.add(h)
        


        
