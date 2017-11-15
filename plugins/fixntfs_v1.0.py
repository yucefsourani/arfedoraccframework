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
import subprocess
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf,GLib, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location, write_file_to_run
from  arfedoraccframework.basepartitions import  get_parttions_by_type
from arfedoraccframework.widgetsutils import Yes_Or_No, NInfo
import time
import threading

button_label         = _("Fix NTFS Partitions")
button_image         = "ntfs_d.jpg"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Fix NTFS Partition")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
    


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.drives_dict = {}
        mainvbox = Gtk.VBox(spacing=20)
        mainvbox.set_margin_left(60)
        mainvbox.set_margin_right(60)
        vbox1 = Gtk.VBox(spacing=20)
        vbox2 = Gtk.VBox(spacing=20)
        
        self._mainbox_.set_border_width(10)
        self._mainbox_.set_spacing(30)
        
        headericon   = get_icon_location("ntfs_d.jpg")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Fix NTFS Partition</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()


        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        
        self.fixbutton = Gtk.Button(_("Run Fix"))
        self.fixbutton.connect("clicked",self.on_fixhbutton_clicked)

        
        self.spinner = Gtk.Spinner()
        
        hboxforcecheckbutton = Gtk.HBox(spacing=3)
        labelforcecheckbutton = Gtk.Label(_("Force\nUmount"))
        labelforcecheckbutton.set_line_wrap(True)
        labelforcecheckbutton.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        labelforcecheckbutton.set_max_width_chars(13)
        labelforcecheckbutton.set_justify(Gtk.Justification.CENTER)
        self.forcecheckbutton = Gtk.CheckButton()
        self.forcecheckbutton.set_active(False)
        self.forcecheckbutton.set_tooltip_text(_("Force Umount"))
        hboxforcecheckbutton.pack_start(labelforcecheckbutton,False,False,0)
        hboxforcecheckbutton.pack_start(self.forcecheckbutton,False,False,0)
        
        combobox = Gtk.HBox(spacing=10)
        refreshbutton = Gtk.Button(_("Refresh"))
        refreshbutton.connect("clicked",self.on_refreshbutton_clicked)
        self.combo = Gtk.ComboBoxText()
        self.on_refreshbutton_clicked()
        self.combo.set_active(0)
        combobox.pack_start(self.combo,True,True,0)
        combobox.pack_start(hboxforcecheckbutton,False,False,0)

        

        vbox2.pack_start(combobox,False,False,0)
        vbox2.pack_start(self.spinner,False,False,0)
        vbox2.pack_start(refreshbutton,False,False,0)
        vbox2.pack_start(self.fixbutton,False,False,0)
        
        
        mainvbox.pack_start(vbox1,False,False,0)
        mainvbox.pack_start(vbox2,False,False,0)
        
        

    def on_refreshbutton_clicked(self,button=None):
        self.combo.remove_all()
        for k,v in self.get_ntfs_p().items():
            self.combo.append(k,v)
        self.combo.set_active(0)
        iter_ = self.combo.get_active_iter()
        if iter_ == None:
            self.fixbutton.set_sensitive(False)
        else:
            self.fixbutton.set_sensitive(True)

    def on_fixhbutton_clicked(self,button):
        iter_ = self.combo.get_active_iter()
        if iter_ == None:
            return
        drive=self.combo.get_model()[iter_][1]
        commands = ["ntfsfix "+drive]
        filetorun = write_file_to_run(commands)
        if not filetorun:
            return
        self._parent_.set_sensitive(False)
        t = threading.Thread(target=self.fix_,args=(filetorun,drive))
        self.drives_dict[drive].umount_(self.forcecheckbutton.get_active())
        t.start()
        
       
    def fix_(self,filetorun,drive):
        GLib.idle_add(self.spinner.start)
        out,err = subprocess.Popen("pkexec bash -e "+filetorun,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        GLib.idle_add(self._parent_.set_sensitive,True)
        if out.strip():
            GLib.idle_add(self.spinner.stop)
            return GLib.idle_add(self.info_,_("Fix Partition {} Sucess.").format(drive))
        else :
            GLib.idle_add(self.spinner.stop)
            err = err.decode("utf-8").strip()
            if err=="Error executing command as another user: Request dismissed":
                return
            if not self.forcecheckbutton.get_active():
                return GLib.idle_add(self.info_,_(err+"\n\n"+"Try Enable Froce Unmout"))
            else:
                return GLib.idle_add(self.info_,err)


    def info_(self,msg):
        info__ = NInfo(msg,self._parent_) 
        info__.start()
        return False
        
    def get_ntfs_p(self):
        drives = get_parttions_by_type(["ntfs"])
        choice = {}
        for k,v in drives.items():
            choice.setdefault(k,k +"   "+"Type "+v[2]+"   "+"Size "+str(int(v[1]/1024/1024))+"MB")
            self.drives_dict.setdefault(k,v[0])
        return choice
         
        
     

        
