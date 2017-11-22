#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  
#  Copyright 2017 youcef sourani <youssef.m.sourani@gmail.com>
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
#  TO DO 
# add yes or no label

import subprocess
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango,GLib
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
import  arfedoraccframework.nv as nvidia
import  arfedoraccframework.basebroadcom as broadcom
from arfedoraccframework.widgetsutils import Yes_Or_No, NInfo
from arfedoraccframework.rpmfusion import installrpmfusion
from arfedoraccframework.runinroot import runinroot
import threading
    
button_label         = _("Drivers Manager")
button_image         = "primary-exec.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Drivers Manager")
blockclose           = False
if_true_skip         = False
if_false_skip        = os.path.isfile("/usr/bin/dnf")
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0

class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.b__ = Gtk.Button()
        self._mainbox_.set_spacing(20)
        self._mainbox_.set_margin_left(100)
        self._mainbox_.set_margin_right(100)
        headericon   = get_icon_location("primary-exec.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Drivers Manager</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()
        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        
        self.statuslabel = Gtk.Label(use_markup=True)
        self.spinner = Gtk.Spinner()
        self._mainbox_.pack_start(self.spinner,True,True,0)
        self._mainbox_.pack_start(self.statuslabel,True,True,0)
        if nvidia.issucureboot():
            self.statuslabel.set_label(_("<b>SecureBoot enabled ,Disable SecureBoot From Bios And Try Again</b>"))
            return
        
        refreshbuttonhbox = Gtk.HBox(spacing=3)
        refreshbuttonhbox.set_homogeneous (True)
        self.refreshbutton = Gtk.Button(_("Refresh MetaData"))
        self.refreshbutton.connect("clicked",self.run_refresh_drivers_files)
        self.refreshbutton2 = Gtk.Button(_("Refresh"))
        self.refreshbutton2.connect("clicked",self.run_refresh_drivers)
        
        refreshbuttonhbox.pack_start(self.refreshbutton,True,True,0)
        refreshbuttonhbox.pack_start(self.refreshbutton2,True,True,0)
        self._mainbox_.pack_start(refreshbuttonhbox,False,False,0)
        
        self.mainhbox = Gtk.HBox()
        self.vb = Gtk.VBox(spacing=20)
        self.mainhbox.add(self.vb)
        self._mainbox_.pack_start(self.mainhbox,False,False,0)
        self.nvidiacard = {}

        
        
    def gui(self):
        h = Gtk.HBox(spacing=30)
        v1 = Gtk.VBox(spacing=2)
        v1.set_homogeneous(True)
        v2 = Gtk.VBox(spacing=2)
        v2.set_homogeneous(True)
        v3 = Gtk.VBox(spacing=2)
        v3.set_homogeneous(True)
        h.pack_start(v1,False,False,0)
        h.pack_start(v2,False,False,0)
        h.pack_start(v3,False,False,0)
        self.vb.pack_start(h,False,False,0)
        for k,v in self.nvidiacard.items():
            nvidiaicon   = get_icon_location("NVLogo_2D.png")
            nvidiapixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(nvidiaicon,100,100)
            nvidiaimage  = Gtk.Image.new_from_pixbuf(nvidiapixbuf)
            l1 = Gtk.Label("<b>"+k+" PCI ID "+v[0]+"</b>",use_markup=True)
            l1.set_line_wrap(True)
            l1.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            if   nvidia.isdual():
                if self.install_or_remove(v[1]):
                    button = Gtk.Button(_("Install"))
                    button.connect("clicked",self.on_install_button_clicked,v[1])
                else:
                    button = Gtk.Button(_("Remove"))
                    button.connect("clicked",self.on_remove_button_clicked,v[1])
            else:
                l = Gtk.Label(_("<b>dual GPU Not Supported</b>"),use_markup=True)
            
            v1.pack_start(nvidiaimage,False,False,0)
            v2.pack_start(l1,False,False,0)
            if   nvidia.isdual():
                v3.pack_start(button,True,False,0)
            else:
                v3.pack_start(l,True,False,0)

        
        
        broadc= broadcom.broadcom()
        if broadc:
            for k,v in broadc.items():
                broadcomicon   = get_icon_location("broadcom_images.jpg")
                broadcompixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(broadcomicon,100,100)
                broadcomimage  = Gtk.Image.new_from_pixbuf(broadcompixbuf)
                l1 = Gtk.Label("<b>"+k+"</b>",use_markup=True)
                l1.set_line_wrap(True)
                l1.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                if self.install_or_remove(v[0]):
                    button = Gtk.Button(_("Install"))
                    button.connect("clicked",self.on_install_button_clicked,v[0])
                else:
                    button = Gtk.Button(_("Remove"))
                    button.connect("clicked",self.on_remove_button_clicked,v[0])
                v1.pack_start(broadcomimage,False,False,0)
                v2.pack_start(l1,False,False,0)
                v3.pack_start(button,True,False,0)
            
        self._parent_.show_all()
        
    def run_refresh_drivers(self,button=None):
        self.mainhbox.remove(self.vb)
        self.vb.destroy()
        del self.vb
        self.vb = Gtk.VBox(spacing=20)
        self.mainhbox.add(self.vb)
        threading.Thread(target=self.refresh_drivers).start()
        
    def refresh_drivers(self):
        self.nvidiacard.clear()
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self._parent_.set_sensitive,False)
        self.d304 = nvidia.drive_304()
        self.d340 = nvidia.drive_340()
        self.d375 = nvidia.drive_375()
        self.d384 = nvidia.drive_384()
        if self.d304 and self.d340 and self.d375 and self.d384:
            self.nvidiacard = nvidia.get_nvidia_driver_name(self.d304,self.d340,self.d375,self.d384)
            
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self._parent_.set_sensitive,True)
        GLib.idle_add(self.gui)
       
    
    def run_refresh_drivers_files(self,button):
        self.mainhbox.remove(self.vb)
        self.vb.destroy()
        del self.vb
        self.vb = Gtk.VBox(spacing=20)
        self.mainhbox.add(self.vb)
        threading.Thread(target=self.refresh_drivers_files).start()
        
    def refresh_drivers_files(self):
        GLib.idle_add(self.refreshbutton.set_label,_("Refresh MetaData"))
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self._parent_.set_sensitive,False)
        if not nvidia.get_drive_304():
            GLib.idle_add(self.refreshbutton.set_label,_("Refresh MetaData Fail"))
            GLib.idle_add(self.spinner.stop)
            GLib.idle_add(self._parent_.set_sensitive,True)
            return
        if not nvidia.get_drive_340():
            GLib.idle_add(self.refreshbutton.set_label,_("Refresh MetaData Fail"))
            GLib.idle_add(self.spinner.stop)
            GLib.idle_add(self._parent_.set_sensitive,True)
            return
        if not nvidia.get_drive_375():
            GLib.idle_add(self.refreshbutton.set_label,_("Refresh MetaData Fail"))
            GLib.idle_add(self.spinner.stop)
            GLib.idle_add(self._parent_.set_sensitive,True)
            return
        if not nvidia.get_drive_384():
            GLib.idle_add(self.refreshbutton.set_label,_("Refresh MetaData Fail"))
            GLib.idle_add(self.spinner.stop)
            GLib.idle_add(self._parent_.set_sensitive,True)
            return
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self._parent_.set_sensitive,True)
        GLib.idle_add(self.run_refresh_drivers)
        
    def install_or_remove(self,packages):
        for p in packages.split():
            if  p=="kernel" or p=="kernel-devel":
                continue
            elif subprocess.call("rpm -q "+repr(p),shell=True)!=0:
                    return True
        return False
        
    def on_remove_button_clicked(self,button,commands):
        yrn = Yes_Or_No(_("No Warranty For This Driver\n\nAre You Sure You Want To Continue ?"),self._parent_)
        if not yrn.check():
            return 
        commands = [i for i in commands.split() if i not in ["kernel","kernel-devel"]]
        commands = " ".join([p for p in commands])
        commands = "dnf remove -y --best "+commands
        self._parent_.set_sensitive(False)
        t = threading.Thread(target=self.install_remove,args=(commands,))
        t.start()
        
    def on_install_button_clicked(self,button,commands):
        yrn = Yes_Or_No(_("No Warranty For This Driver\n\nAre You Sure You Want To Continue ?"),self._parent_)
        if not yrn.check():
            return 
        commands = "dnf install -y --best  "+commands
        self._parent_.set_sensitive(False)
        t = threading.Thread(target=self.install_remove,args=(commands,))
        t.start()

    def install_remove(self,command):
        GLib.idle_add(self.spinner.start)
        GLib.idle_add(self.statuslabel.set_label,_("<b>Please Wait</b>"))
        d = installrpmfusion()
        if d!=0 :
            GLib.idle_add(self.statuslabel.set_label,_("<b>Install Rpmfusion Repos Fail</b>"))
            self.run_refresh_drivers()
            return
        out = runinroot.call(command,timeout=1000000)
        if out==0:
            GLib.idle_add(self.statuslabel.set_label,_("<b>Success Restart System</b>"))
        else:
            GLib.idle_add(self.statuslabel.set_label,_("<b>Fail</b>"))
        self.run_refresh_drivers()
        
