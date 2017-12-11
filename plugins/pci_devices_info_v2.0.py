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
import subprocess
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location

button_label         = _("PCI Devices Info")
button_image         = "exec-icon.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Get PCI Dives Info")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-utilities"

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
        headerlabel  = Gtk.Label(_("<b>Get PCI Devices Info</b>"),use_markup=True)
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
        treestore = Gtk.TreeStore(str)
        pci_info = self.get_pci_info()
        for info in pci_info:
            info = info.strip()
            if info.startswith("Slot:"):
                info = pci_info[pci_info.index(info)+3].split(":",1)[-1].strip()
                info = info[::-1].split("[",1)[-1]
                tag_ = treestore.append(None, [info[::-1]])
                continue
            treestore.append(tag_, [info])

        treeview = Gtk.TreeView()
        treeview.set_model(treestore)
        mainvbox.pack_start(treeview,False,False,0)

        cellrenderertext = Gtk.CellRendererText()

        treeviewcolumn = Gtk.TreeViewColumn("PCI Devices")
        treeview.append_column(treeviewcolumn)
        treeviewcolumn.pack_start(cellrenderertext, True)
        treeviewcolumn.add_attribute(cellrenderertext, "text", 0)

    def get_pci_info(self):
        return subprocess.check_output("lspci -vvvnnkmm",shell=True).decode("utf-8").split("\n")
