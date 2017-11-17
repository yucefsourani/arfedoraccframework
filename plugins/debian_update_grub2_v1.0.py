#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
from arfedoraccframework.widgetsutils import RunTextView

button_label         = _("Update Grub2 Menu")
button_image         = "1200px-Tux.svg.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Update Grub2 Boot Loader Menu")
blockclose           = False
if_true_skip         = False
if_false_skip        = os.path.isfile("/usr/sbin/update-grub")
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(5)
        self._mainbox_.set_spacing(20)
        h = Gtk.HBox()
        h.set_homogeneous (True)
        v = Gtk.VBox()

        
        headericon   = get_icon_location("1200px-Tux.svg.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Update Boot Loader Menu</b>"),use_markup=True)
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
        self.t = RunTextView (self._parent_,True,[["pkexec  /usr/sbin/update-grub","free",True]],\
        cursor_visible=True,end="\n",justification=Gtk.Justification.CENTER,spinner=self.spinner)
        self.t.set_size_request (200,200)
        button = Gtk.Button(_("Update"))
        button.connect("clicked",self.on_button_clicked)
        
        
        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        h.pack_start(button,False,False,0)
        v.pack_start(self.t,False,False,0)
        self._mainbox_.pack_start(h,False,False,0)
        self._mainbox_.pack_start(self.spinner,False,False,0)
        self._mainbox_.pack_start(v,False,False,0)
        

    def on_button_clicked(self,button):
        self.t.start()
        
        
