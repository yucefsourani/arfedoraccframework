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
import subprocess
import collections
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
import arfedoraccframework.basesystemd as systemd
import time


button_label         = _("Service Manager")
button_image         = "tux_images.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Systemd Service Manager")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-system"


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_spacing(25)
        self.gui_()
        
    def gui_(self):
        self.system_systemd = systemd.SystemDSystem()
        self.user_systemd = systemd.SystemDUser()
        self.system_enabled_disabled_service = collections.OrderedDict(sorted(self.system_systemd.get_all_service_timer_enabled_disabled_unit_files_dict().items()))
        self.user_enabled_disabled_service = collections.OrderedDict(sorted(self.user_systemd.get_all_service_timer_enabled_disabled_unit_files_dict().items()))

        headericon   = get_icon_location("SYSTEMD-e1434229775958.gif")
        self.headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>SystemD Service Manager</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        self.headerbox.pack_start(headerimage,False,False,0)
        self.headerbox.pack_start(headerlabel,False,False,0)
        self._mainbox_.pack_start(self.headerbox,False,False,0)


        
        self.mainhbox = Gtk.HBox()
        vbox     = Gtk.VBox(spacing=20)
        self.mainhbox.pack_start(vbox,True,False,0)
        self._mainbox_.pack_start(self.mainhbox,False,False,0)

        if len(self.user_enabled_disabled_service.items())!=0:
            usertitlehbox = Gtk.HBox()
            user_edhbox = Gtk.HBox()
            user_sthbox = Gtk.HBox()
        
            usertitle = Gtk.Label(_("<b>Services Name</b>"),use_markup=True)
            user_ed = Gtk.Label(_("<b>Enable/Disable</b>"),use_markup=True)
            user_st = Gtk.Label(_("<b>Start/Stop</b>"),use_markup=True)

            usertitlehbox.pack_start(usertitle,False,False,0)
            user_edhbox.pack_start(user_ed,False,False,0)
            user_sthbox.pack_start(user_st,False,False,0)
        
            userlabel = Gtk.Label(_("<b>User Services</b>"),use_markup=True)
            searchicon = Gtk.Image()
            searchicon.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.BUTTON)
            self.searchbutton = Gtk.ToggleButton()
            self.searchbutton.add(searchicon)
            hboxbutton = Gtk.HBox()
            hboxbutton.pack_start(self.searchbutton,True,False,0)
            self.searchbutton.connect("toggled", self._on_transition1)
            self.revealer1 = Gtk.Revealer()
            hboxrevealer = Gtk.HBox()
            hboxrevealer.pack_start(self.revealer1,True,False,0)
            self.entry1 = Gtk.SearchEntry(placeholder_text="Search Service")
            self.entry1.props.margin_left = 15
            self.entry1.props.margin_right = 15
            self.entry1.props.margin_top = 5
            self.entry1.props.margin_bottom = 5
            self.entry1.connect("search-changed", self._on_search1)
            self.revealer1.add(self.entry1)
            
            uservseparator = Gtk.Separator()
            uservseparator.set_margin_top(30)
            h = Gtk.HBox()
            h.set_homogeneous (True)
            h.pack_start(usertitlehbox,True,True,0)
            h.pack_start(user_edhbox,True,False,0)
            h.pack_start(user_sthbox,True,False,0)
            vbox.pack_start(uservseparator,False,False,0)
            vbox.pack_start(userlabel,False,False,0)
            vbox.pack_start(hboxbutton,False,False,0)
            vbox.pack_start(hboxrevealer,False,False,0)
            vbox.pack_start(h,False,False,0)
            self.listbox1 = Gtk.ListBox()
            self.listbox1.set_filter_func(self._list_filter_func1, None)
            vbox.pack_start(self.listbox1,False,False,0)
            for k,v in self.user_enabled_disabled_service.items():
                row = Gtk.ListBoxRow(activatable=True)
                self.listbox1.add(row)
                h = Gtk.HBox()
                row.add(h)
                h.set_homogeneous (True)
                labelhbox = Gtk.HBox()
                label  = Gtk.Label(k)
                label.set_selectable(True)
                label.set_line_wrap(True)
                label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                label.set_max_width_chars(40)
                labelhbox.pack_start(label,False,True,0)
                if  v[0]=="disabled":
                    self.switch=Gtk.Switch()
                else:
                    self.switch=Gtk.Switch()
                    self.switch.set_active(True)
                if  v[1][3]!="active":
                    self.switch_=Gtk.Switch()
                else:
                    self.switch_=Gtk.Switch()
                    self.switch_.set_active(True)
                
                self.switchhandler=self.switch.connect("state-set",self.on_switch_changed_user_enable_disable,k)
                self.switchhandler_=self.switch_.connect("state-set",self.on_switch_changed_user_start_stop,k)
                switchhbox = Gtk.HBox()
                switchhbox_ = Gtk.HBox()
                switchhbox.pack_start(self.switch,True,False,0)
                switchhbox_.pack_start(self.switch_,True,False,0)
                h.pack_start(labelhbox,True,True,0)
                h.pack_start(switchhbox,True,True,0)
                h.pack_start(switchhbox_,True,True,0)
                

        


        if len(self.system_enabled_disabled_service.items())!=0:
            systemtitlehbox = Gtk.HBox()
            system_edhbox = Gtk.HBox()
            system_sthbox = Gtk.HBox()
        
            systemtitle = Gtk.Label(_("<b>Services Name</b>"),use_markup=True)
            system_ed = Gtk.Label(_("<b>Enable/Disable</b>"),use_markup=True)
            system_st = Gtk.Label(_("<b>Start/Stop</b>"),use_markup=True)
        
            systemtitlehbox.pack_start(systemtitle,False,False,0)
            system_edhbox.pack_start(system_ed,False,False,0)
            system_sthbox.pack_start(system_st,False,False,0)
            
            systemlabel = Gtk.Label(_("<b>System Services</b>"),use_markup=True)
            searchicon = Gtk.Image()
            searchicon.set_from_icon_name("edit-find-symbolic", Gtk.IconSize.BUTTON)
            searchbutton = Gtk.ToggleButton()
            searchbutton.add(searchicon)
            hboxbutton = Gtk.HBox()
            hboxbutton.pack_start(searchbutton,True,False,0)
            searchbutton.connect("toggled", self._on_transition2)
            self.revealer2 = Gtk.Revealer()
            hboxrevealer = Gtk.HBox()
            hboxrevealer.pack_start(self.revealer2,True,False,0)
            self.entry2 = Gtk.SearchEntry(placeholder_text="Search Service")
            self.entry2.props.margin_left = 15
            self.entry2.props.margin_right = 15
            self.entry2.props.margin_top = 5
            self.entry2.props.margin_bottom = 5
            self.entry2.connect("search-changed", self._on_search2)
            self.revealer2.add(self.entry2)
            
            systemvseparator = Gtk.Separator()
            systemvseparator.set_margin_top(30)
            h = Gtk.HBox()
            h.set_homogeneous (True)
            h.pack_start(systemtitlehbox,True,True,0)
            h.pack_start(system_edhbox,True,False,0)
            h.pack_start(system_sthbox,True,False,0)
            vbox.pack_start(systemvseparator,False,False,0)
            vbox.pack_start(systemlabel,False,False,0)
            vbox.pack_start(hboxbutton,False,False,0)
            vbox.pack_start(hboxrevealer,False,False,0)
            vbox.pack_start(h,False,False,0)
            self.listbox2 = Gtk.ListBox()
            self.listbox2.props.margin_bottom=150
            self.listbox2.set_filter_func(self._list_filter_func2, None)
            vbox.pack_start(self.listbox2,False,False,0)
            for k,v in self.system_enabled_disabled_service.items():
                row2 = Gtk.ListBoxRow(activatable=True)
                self.listbox2.add(row2)
                h = Gtk.HBox()
                row2.add(h)
                h.set_homogeneous (True)
                labelhbox2 = Gtk.HBox()
                label2  = Gtk.Label(k)
                label2.set_selectable(True)
                label2.set_line_wrap(True)
                label2.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                label2.set_max_width_chars(40)
                labelhbox2.pack_start(label2,False,True,0)
                if  v[0]=="disabled":
                    self.switch2=Gtk.Switch()
                else:
                    self.switch2=Gtk.Switch()
                    self.switch2.set_active(True)
                if  v[1][3]!="active":
                    self.switch2_=Gtk.Switch()
                else:
                    self.switch2_=Gtk.Switch()
                    self.switch2_.set_active(True)
                
                self.switchhandler2=self.switch2.connect("state-set",self.on_switch_changed_system_enable_disable,k)
                self.switchhandler2_=self.switch2_.connect("state-set",self.on_switch_changed_system_start_stop,k)
                switchhbox2 = Gtk.HBox()
                switchhbox2_ = Gtk.HBox()
                switchhbox2.pack_start(self.switch2,True,False,0)
                switchhbox2_.pack_start(self.switch2_,True,False,0)
                h.pack_start(labelhbox2,True,True,0)
                h.pack_start(switchhbox2,True,True,0)
                h.pack_start(switchhbox2_,True,True,0)
                
                
        


    
    def refresh_(self):
        self._mainbox_.remove(self.headerbox)
        self._mainbox_.remove(self.mainhbox)
        self.headerbox.destroy()
        self.mainhbox.destroy()
        self.gui_()
        self._parent_.show_all()
    

    def on_switch_changed_system_enable_disable(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec systemctl enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_enable_disable)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_system_enable_disable)
                return True
                    
        else :
            check = subprocess.call("pkexec systemctl disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_enable_disable)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_system_enable_disable)
                return True
        self.refresh_()
        return True
    
    def on_switch_changed_user_enable_disable(self,switch,state,reponame):
        if state:
            check = subprocess.call("systemctl --user enable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_enable_disable)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_user_enable_disable)
                return True
                    
        else :
            check = subprocess.call("systemctl --user  disable "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_enable_disable)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_user_enable_disable)
                return True
        self.refresh_()
        return True
     
        


    def on_switch_changed_system_start_stop(self,switch,state,reponame):
        if state:
            check = subprocess.call("pkexec systemctl start "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_start_stop)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_system_start_stop)
                return True
                    
        else :
            check = subprocess.call("pkexec systemctl stop "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_system_start_stop)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_system_start_stop)
                return True
        self.refresh_()
        return True
    
    def on_switch_changed_user_start_stop(self,switch,state,reponame):
        if state:
            check = subprocess.call("systemctl --user start "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_start_stop)
                switch.set_active(False)
                switch.handler_unblock_by_func(self.on_switch_changed_user_start_stop)
                return True
                    
        else :
            check = subprocess.call("systemctl --user  stop "+reponame,shell=True)
            if check!=0:
                switch.handler_block_by_func(self.on_switch_changed_user_start_stop)
                switch.set_active(True)
                switch.handler_unblock_by_func(self.on_switch_changed_user_start_stop)
                return True
        self.refresh_()
        return True


    def _on_search1(self, entry):
        self.listbox1.invalidate_filter()
    
    def _list_filter_func1(self, lista, user_data):
        text = self.entry1.get_text()
        if not text:
            return lista
        lbl = lista.get_child().get_children()[0].get_children()[0]
        if text.lower() in lbl.get_text().lower():
            return lista   
        
               
    def _on_transition1(self, btn):
        if self.revealer1.get_reveal_child():
            self.revealer1.set_reveal_child(False) 
            self.entry1.set_text("") 
            btn.grab_focus()      
        else:
            self.revealer1.set_reveal_child(True)
            self.entry1.grab_focus()
    
    def _on_search2(self, entry):
        self.listbox2.invalidate_filter()
    
    def _list_filter_func2(self, lista, user_data):
        text = self.entry2.get_text()
        if not text:
            return lista
        lbl = lista.get_child().get_children()[0].get_children()[0]
        if text.lower() in lbl.get_text().lower():
            return lista   
        
               
    def _on_transition2(self, btn):
        if self.revealer2.get_reveal_child():
            self.revealer2.set_reveal_child(False) 
            self.entry2.set_text("") 
            btn.grab_focus()      
        else:
            self.revealer2.set_reveal_child(True)
            self.entry2.grab_focus()
    
