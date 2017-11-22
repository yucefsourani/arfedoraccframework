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
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GdkPixbuf,GLib, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
import arfedoraccframework.basefonts as font


button_label         = _("Manager Arabic Fonts")
button_image         = "kacsttitle.gif"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Manager Arabic Fonts")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
    


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self._mainbox_.set_border_width(10)
        self._mainbox_.set_spacing(30)
        headericon   = get_icon_location("kacsttitle.gif")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Manager Arabic Fonts</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()
        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        
        self.mainhbox = Gtk.HBox()
        self.vb       = Gtk.HBox()
        self._mainbox_.pack_start(self.mainhbox,True,True,0)
        self.mainhbox.pack_start(self.vb,True,True,0)
        self.gui()
    
    def  gui(self):
        count=0
        font_dict = {}
        self.combo = Gtk.ComboBoxText()
        self.combo.remove_all()
        self.combo.append(str(count),"None")
        font_dict.setdefault("None",count)
        count+1
        for fontname in font.get_fonts_name("ar"):
            self.combo.append(str(count),fontname)
            font_dict.setdefault(fontname,count)
            count+=1
        fn = font.get_config()
        if fn:
            self.combo.set_active(font_dict[fn]+1)
        else:
            self.combo.set_active(0)
        self.combo.connect("changed",self.on_combo_changed)
        self.vb.pack_start(self.combo,True,True,0)
        self._parent_.show_all()
        
        
    def on_combo_changed(self,combo):
        iter_ = self.combo.get_active_iter()
        if iter_ == None:
            return
        fntn=self.combo.get_model()[iter_][0]
        if fntn == "None":
            font.remove_config()
        else:
            check = font.set_config(fntn)

