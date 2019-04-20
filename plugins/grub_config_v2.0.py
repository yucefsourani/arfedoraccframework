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
#
import os  
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango, GLib
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location, fedora_get_grub_menufile, get_file_to_run,get_distro_name,get_distro_version
from collections import OrderedDict
from arfedoraccframework.runinroot import runinroot
from arfedoraccframework.widgetsutils import Yes_Or_No
import threading
import time

button_label         = _("Config Grub2")
button_image         = "1200px-Tux.svg.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Config Grub2 Boot Loader")
blockclose           = False
if_true_skip         = False
if_false_skip        = os.path.isfile("/etc/fedora-release")
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-utilities" 


def fedora_30():
    if get_distro_name()=="fedora":
        if get_distro_version()=="30":
            return True
        else:
            return False
    else:
        return False
    
class copy_config_and_apply(threading.Thread):
    def __init__(self,file_,parent,spinner,refresh_func):
        threading.Thread.__init__(self)
        self.file_        = file_
        self.parent       = parent
        self.spinner      = spinner
        self.refresh_func = refresh_func
        
    def run(self):
        GLib.idle_add(self.parent.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        grubmenuconfig = fedora_get_grub_menufile()
        check = runinroot.call("cp {} /etc/default/grub && /usr/sbin/grub2-mkconfig -o  {}".format(self.file_,grubmenuconfig))
        GLib.idle_add(self.parent.set_sensitive,True)
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.refresh_func)

            
class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(5)
        self._mainbox_.set_spacing(20)
        
        headericon   = get_icon_location("1200px-Tux.svg.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        if fedora_30():
            headerlabel  = Gtk.Label(_("<b>Config Boot Loader\n(Fedora 30 detected  some options maybe not working like GRUB_CMDLINE_LINUX )\n<span  foreground=\"red\">Be Careful</span></b>"),use_markup=True)
        else:
            headerlabel  = Gtk.Label(_("<b>Config Boot Loader\n<span  foreground=\"red\">Be Careful</span></b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()
        headervseparator.set_margin_bottom(10)
        headervseparator.set_margin_top(30)
        self.spinner = Gtk.Spinner()
        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        self._mainbox_.pack_start(self.spinner,False,False,0)
        self.vb=Gtk.VBox(spacing=10)
        self._mainbox_.pack_start(self.vb,True,False,0)
        self.gui()
        
    def gui(self):
        grub_config = self.get_grub_config()
        self.liststore = Gtk.ListStore(str, str)
        self.liststore.clear()
        for k,v in grub_config.items():
            self.liststore.append([k, v])

        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        self.vb.pack_start(treeview,True,True,0)

        cellrenderertext = Gtk.CellRendererText(placeholder_text="Add Config Key...")
        cellrenderertext.set_property("editable", True)
        cellrenderertext.connect("edited", self.on_cell_edited,0)
        treeviewcolumn = Gtk.TreeViewColumn(_("Keys"))
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.set_fixed_width(399)
        treeviewcolumn.set_min_width(30)
        treeviewcolumn.set_max_width(400)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)
        treeview.append_column(treeviewcolumn)

        cellrenderertext = Gtk.CellRendererText(placeholder_text="Add Config Value...")
        cellrenderertext.set_property("editable", True)
        cellrenderertext.connect("edited", self.on_cell_edited,1)

        treeviewcolumn = Gtk.TreeViewColumn(_("Values"))
        treeviewcolumn.set_resizable(True)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 1)
        treeview.append_column(treeviewcolumn)
        
        buttonbox = Gtk.ButtonBox()
        buttonbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        buttonbox.set_spacing(2)
        
        applybutton=Gtk.Button(_("Apply"))
        applybutton.connect("clicked",self.on_button_clicked)
        buttonbox.add(applybutton)
        
        reloadbutton=Gtk.Button(_("Reload"))
        reloadbutton.connect("clicked",self.refresh_)
        buttonbox.add(reloadbutton)
        self.vb.pack_start(buttonbox,False,False,0)

    def refresh_(self,button=None):
        self._mainbox_.remove(self.vb)
        self.vb.destroy()
        self.vb=Gtk.VBox(spacing=10)
        self._mainbox_.pack_start(self.vb,False,False,0)
        self.gui()
        self._parent_.show_all()
        
    def on_button_clicked(self,button):
        yrn = Yes_Or_No(_("Warning !! change grub config on your own risk\n\nAre You Sure You Want To Continue ?"),self._parent_)
        if not yrn.check():
            return 
        result = []
        try:
            for i in  self.liststore:
                if not i[0] or not i[1]:
                    continue
                result.append(i[0]+"="+i[1]+"\n")
        except Exception as e:
            print(e)
            self.refresh_()
            return False
            
        self.write_config_for_file(result)
        
    def write_config_for_file(self,config):
        file_ = get_file_to_run(add="grubconfig")
        try:
            with open(file_,"w") as mf:
                for line in config:
                    mf.write(line)
        except Exception as e:
            print(e)
            self.refresh_()
            return False
        copy_config_and_apply(file_,self._parent_,self.spinner,self.refresh_).start()
                
            
    def on_cell_edited(self, cellrenderertext, treepath, text,number):
        self.liststore[treepath][number] = text


    def get_grub_config(self):
        result = OrderedDict()
        with open("/etc/default/grub") as mf:
            for line in mf:
                line = line.strip()
                if line:
                    if line.startswith("#"):
                        if "=" not in line:
                            continue
                        else:
                            if not line.replace(" ","")[1:3].isupper():
                                continue
                    splitline = line.split("=",1)
                    k_ = splitline[0].strip()
                    v_ = splitline[1].strip()
                    result.setdefault(k_,v_)
        result.setdefault("","")
        return result
