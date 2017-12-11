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
import os
import sys
import pwd
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location


button_label         = _("Get Exec")
button_image         = "exec-icon.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Get Exec From Desktop Entry")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-utilities" 

def get_bin_path(command):
    path = [p for p in os.environ["PATH"].split(":") if os.path.isdir(p)]
    result = _("Not Available")
    for location in path:
        try:
            for dirname,dirs,files in os.walk(location):
                for file_ in files:
                    if file_ == command:
                        file_ = os.path.join(dirname,file_)
                        if os.path.isfile(file_):
                            result = file_
        except:
            continue
    return result
                    

def parse_desktop_entry_file(name,desktopentryfile):
    result = {}
    name = name.replace(" ","").lower()
    try:
        with open(desktopentryfile) as mf:
            for line in mf:
                if line:
                    try:
                        line = line.split("=",1)
                        result.setdefault(line[0].strip(),line[1].strip())
                    except:
                        continue
    except:
        return False
    if name == "*":#disable this options
        name = ""
    if name == "*":
        try:
            if "Name" in result.keys() and "Exec" in result.keys():
                exec__ = result["Exec"]
                return [result["Name"],[exec__],get_bin_path(exec__.split()[0]),desktopentryfile]
        except:
            return False
    else:    
        try:
            if "Name" in result.keys() and "Exec" in result.keys():
                if name == result["Name"].replace(" ","").lower():
                    exec__ = result["Exec"]
                    return [result["Name"],[exec__],get_bin_path(exec__.split()[0]),desktopentryfile]
        except:
            return False
    return False
    
                

def read_all_desktop_entry_files(name):
    home = pwd.getpwuid(os.geteuid()).pw_dir
    locations = [os.path.join(home,".local/share/applications"),
                 os.path.join(home,".local/share/flatpak/exports/share/applications"),
                 "/usr/share/applications",
                 "/usr/local/share/applications",
                 "/var/lib/flatpak/exports/share/"]
                 
    locations = [l for l in locations if os.path.isdir(l)]
    result = []
    for location in locations:
        for dirname,dirs,files in os.walk(location):
            for file_ in files:
                desktopentryfile = os.path.join(dirname,file_)
                if desktopentryfile.endswith(".desktop"):
                    check = parse_desktop_entry_file(name,desktopentryfile)
                    if check :
                        if len(result)!=0:
                            result[0][1].append(check[1])
                            result[0][2]+=" &&  "+check[2]
                            result[0][3]+=" &&  "+check[3]
                        else:
                            result.append(check)
                        
    return result

class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(5)
        
        mainvbox = Gtk.VBox(spacing=20)
        mainvbox.set_border_width(10)
        mainvbox.set_margin_left(100)
        mainvbox.set_margin_right(100)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        headericon   = get_icon_location("primary-exec.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Get Exec</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        mainvbox.pack_start(headerbox,False,False,0)
        vseparator = Gtk.Separator()
        vseparator.set_margin_top(10)
        mainvbox.pack_start(vseparator,False,False,0)
        
        vb = Gtk.VBox(spacing=10)
        hb = Gtk.HBox(spacing=10)
        vmainbox = Gtk.VBox(spacing=30)
        hbox1 = Gtk.HBox(spacing=10)
        hbox2 = Gtk.HBox(spacing=10)
        hbox3 = Gtk.HBox(spacing=10)
        hbox4 = Gtk.HBox(spacing=10)
        hbox5 = Gtk.HBox(spacing=10)
        hbox6 = Gtk.HBox(spacing=10)
        hbox0 = Gtk.HBox(spacing=10)
        
        self.filenameentry = Gtk.Entry()
        self.filenameentry.set_placeholder_text(_("Enter Program Name..."))
        self.filenameentry.set_max_length(63)
        
        argv_check_vbox = Gtk.VBox(spacing=2)
        argv_label= Gtk.Label("argv")
        self.argv_check = Gtk.CheckButton()
        self.argv_check.set_tooltip_text(_("Get Command with  argv"))
        self.argv_check.set_active(True) 


        self.label1 = Gtk.Label(_("Name : "))
        self.label2 = Gtk.Label(_("Command : "))
        self.label3 = Gtk.Label(_("Path : "))
        self.label0 = Gtk.Label(_("File : "))
        
        self.label1.set_line_wrap(True)
        self.label2.set_line_wrap(True)
        self.label3.set_line_wrap(True)
        self.label0.set_line_wrap(True)


        self.label1_ = Gtk.Label()
        self.label2_ = Gtk.Label()
        self.label3_ = Gtk.Label()
        self.label0_ = Gtk.Label()
        
        self.label1_.set_line_wrap(True)
        self.label2_.set_line_wrap(True)
        self.label3_.set_line_wrap(True)
        self.label0_.set_line_wrap(True)
        self.label1_.set_selectable(True)
        self.label2_.set_selectable(True)
        self.label3_.set_selectable(True)
        self.label0_.set_selectable(True)
        
        
        button_vbox = Gtk.VBox(spacing=5)
        run_button = Gtk.Button(_("Get"))
        run_button.connect("clicked",self.on_run_button_clicked)
        
        argv_check_vbox.pack_start(argv_label,True,True,0)
        argv_check_vbox.pack_start(self.argv_check,True,True,0)
        hbox1.pack_start(self.filenameentry,True,True,0)
        hbox1.pack_start(argv_check_vbox,False,False,0)
        
        hbox2.pack_start(self.label1,False,False,0)
        hbox2.pack_start(self.label1_,False,False,0)
        hbox3.pack_start(self.label2,False,False,0)
        hbox3.pack_start(self.label2_,False,False,0)
        hbox4.pack_start(self.label3,False,False,0)
        hbox4.pack_start(self.label3_,False,False,0)
        hbox0.pack_start(self.label0,False,False,0)
        hbox0.pack_start(self.label0_,False,False,0)
        hbox5.pack_start(run_button,True,True,0)



        
        button_vbox.pack_start(hbox5,True,True,0)

        
        vmainbox.pack_start(hbox1,True,True,0)
        vmainbox.pack_start(hbox2,True,True,0)
        vmainbox.pack_start(hbox3,True,True,0)
        vmainbox.pack_start(hbox4,True,True,0)
        vmainbox.pack_start(hbox0,True,True,0)
        vmainbox.pack_start(button_vbox,True,True,0)
        hb.pack_start(vmainbox,True,True,0)
        vb.pack_start(hb,True,True,0)
        mainvbox.pack_start(vb,False,False,0)
        vseparator = Gtk.Separator()
        vseparator.set_margin_top(10)
        mainvbox.pack_start(vseparator,False,False,0)

        
    def on_run_button_clicked(self,button):		
        name = self.filenameentry.get_text()
        if  name:
            result = read_all_desktop_entry_files(name)
            if len(result) != 0:
                self.label1_.set_label(result[0][0])
                if len(result[0][1])>1:
                    if self.argv_check.get_active() and len(result[0][1])>1:
                        self.label2_.set_label(result[0][1][0]+" && "+" && ".join(l for i in result[0][1][1:] for l in i))
                    else:
                        self.label2_.set_label(result[0][1][0]+" && "+" && ".join(l.split()[0] for i in result[0][1][1:] for l in i))
                else:
                    if self.argv_check.get_active():
                        self.label2_.set_label(result[0][1][0])
                    else:
                        self.label2_.set_label(result[0][1][0].split()[0])
                self.label3_.set_label(result[0][2])
                self.label0_.set_label(result[0][3])

                    
            else:
                self.label1_.set_label(name)
                self.label2_.set_label("Unknown")
                self.label3_.set_label("Unknown")
                self.label0_.set_label("Unknown")
        else:
            self.label1_.set_label("Unknown")
            self.label2_.set_label("Unknown")
            self.label3_.set_label("Unknown")
            self.label0_.set_label("Unknown")

        
