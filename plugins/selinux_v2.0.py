#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  selinux_v1.0.py
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
#
import subprocess
import os
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location, get_file_to_run,write_file_to_run


def get_selinux_mode():
    with open("/etc/selinux/config") as myfile: 
        for line in myfile.readlines():
            line = line.strip()
            if line.replace(" ","").startswith("SELINUX="):
                return line.split("=",1)[1].strip()
    return False
    
button_label         = _("Selinux Manager")
button_image         = "selinux-penguin-new_medium.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Selinux Manager")
blockclose           = False
if_true_skip         = False
if_false_skip        = os.path.isfile("/etc/selinux/config")
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-system"

def set_selinux_mode(oldmode,newmode):
    result = ""
    with open("/etc/selinux/config") as myfile: 
        for line in myfile.readlines():
            line = line.strip()
            if line.replace(" ","").startswith("SELINUX="):
                state = line.split("=",1)[1].strip()
                if state=="disabled":
                    return False
                elif state == oldmode:
                    line = "SELINUX="+newmode
            result+=line+"\n"

    return result




class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.gui()
        
    def gui(self):
        if get_selinux_mode()=="disabled":
            l = Gtk.Label(_("Selinux Is Disabled Nothing To Do"))
            self._mainbox_.pack_start(l,True,True,0)
        else:
            self.mainvbox = Gtk.VBox(spacing=20)
            self.mainvbox.set_margin_left(90)
            self.mainvbox.set_margin_right(90)
            self._mainbox_.set_border_width(5)
            self._mainbox_.pack_start(self.mainvbox,False,False,0)
            headericon   = get_icon_location("selinux-penguin-new_medium.png")
            headerbox    = Gtk.VBox(spacing=6)
            headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
            headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
            headerlabel  = Gtk.Label(_("<b>Selinux Manager</b>"),use_markup=True)
            headerlabel.set_line_wrap(True)
            headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            headerlabel.set_max_width_chars(13)
            headerlabel.set_justify(Gtk.Justification.CENTER)
            headerbox.pack_start(headerimage,False,False,0)
            headerbox.pack_start(headerlabel,False,False,0)
            headervseparator = Gtk.Separator()
            headervseparator.set_margin_bottom(30)
            self.mainvbox.pack_start(headerbox,False,False,0)
            self.mainvbox.pack_start(headervseparator,False,False,0)

            h_ = Gtk.HBox(spacing=10)
            hh_ = Gtk.HBox(spacing=10)
            h_.set_homogeneous (True)
            vi = Gtk.VBox(spacing=5)
            v_ = Gtk.VBox(spacing=5)
            logo__ = get_icon_location("com.mrbimc.selinux.20171031.png")
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(logo__,100,100)
            image  = Gtk.Image.new_from_pixbuf(pixbuf)
            
            label  = Gtk.Label(_("<b>Set And Apply Selinux Mode</b>"),use_markup=True)
            #label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label.set_justify(Gtk.Justification.CENTER)
            
            
            self.button1 = Gtk.RadioButton.new_with_label_from_widget(None, _("Enforcing"))


            self.button2 = Gtk.RadioButton.new_from_widget(self.button1)
            self.button2.set_label(_("Permissive"))
            if get_selinux_mode()=="enforcing":
                self.button1.set_active(True)
            else:
                self.button2.set_active(True)
            self.button1.connect("toggled", self.on_button_toggled)
            self.button2.connect("toggled", self.on_button_toggled)
            v_.pack_start(label, False, False, 0)
            v_.pack_start(self.button1, False, False, 0)
            v_.pack_start(self.button2, False, False, 0)
            vi.pack_start(image, False, False, 0)
            hh_.pack_start(vi, False, False, 0)
            hh_.pack_start(v_, False, False, 0)
            h_.pack_start(hh_, False, False, 0)
            self.mainvbox.pack_start(h_, False, False, 0)
        self._parent_.show_all()
        
    def on_button_toggled(self,button):
        if get_selinux_mode()=="disabled":
            self._mainbox_.remove(self.mainvbox)
            self.mainvbox.destroy()
            self.gui()
            return
            
        if self.button1.get_active():
            towrite = set_selinux_mode("permissive","enforcing")
            if not towrite:
                self._mainbox_.remove(self.mainvbox)
                self.mainvbox.destroy()
                self.gui()
                return
            file_source = get_file_to_run()
            with open(file_source,"w") as mf:
                mf.write(towrite)
            filetorun = write_file_to_run(["cp {} /etc/selinux/config".format(file_source),"setenforce 1"],add="enforcing")
            subprocess.call("pkexec bash -e  {}".format(filetorun),shell=True)
        
        else:
            towrite = set_selinux_mode("enforcing","permissive")
            if not towrite:
                self._mainbox_.remove(self.mainvbox)
                self.mainvbox.destroy()
                self.gui()
                return
            file_source = get_file_to_run()
            with open(file_source,"w") as mf:
                mf.write(towrite)
            filetorun = write_file_to_run(["cp {} /etc/selinux/config".format(file_source),"setenforce 0"],add="permissive")
            subprocess.call("pkexec bash -e  {}".format(filetorun),shell=True)
            




        self._mainbox_.remove(self.mainvbox)
        self.mainvbox.destroy()
        self.gui()
