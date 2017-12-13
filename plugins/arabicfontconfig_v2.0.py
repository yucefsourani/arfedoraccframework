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
category             = _("Personal")
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
category_icon_theme  = "preferences-desktop-personal"


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
        self.spinner  = Gtk.Spinner()
        self._mainbox_.pack_start(headerbox,False,False,0)
        self._mainbox_.pack_start(headervseparator,False,False,0)
        self._mainbox_.pack_start(self.spinner,False,False,0)
        self.gui()
    
    def  gui(self):
        self.mainhbox = Gtk.HBox()
        self.vb1      = Gtk.VBox(spacing=10)
        self.vb2      = Gtk.VBox(spacing=10)
        self._mainbox_.pack_start(self.mainhbox,True,True,0)
        self.mainhbox.pack_start(self.vb1,True,True,0)
        self.mainhbox.pack_start(self.vb2,True,True,0)
        count=0
        self.addfontlabel = Gtk.Label(_("Add Fonts From Folder"))
        self.addfontbutton = Gtk.Button(_("Select"))
        self.vb1.pack_start(self.addfontlabel,True,True,0)
        self.vb2.pack_start(self.addfontbutton,False,False,0)
        self.addfontbutton.connect("clicked",self.on_addfontbutton_clicked)
        font_dict = {}
        font_dict.clear()
        self.combo = Gtk.ComboBoxText()
        self.combo.remove_all()
        self.combo.append(str(count),"None")
        font_dict.setdefault("None",count)
        count+1
        for fontname in font.get_fonts_name("ar"):
            self.combo.append(str(count),fontname)
            font_dict.setdefault(fontname,count)
            count+=1
        self.label = Gtk.Label("بسم الله الرحمن الرحيم")
        fn = font.get_config()
        if fn:
            self.combo.set_active(font_dict[fn]+1)
            pangofont = Pango.font_description_from_string(fn)
            self.label.modify_font(pangofont)
        else:
            self.combo.set_active(0)
        self.combo.connect("changed",self.on_combo_changed)
        self.vb1.pack_start(self.label,True,True,0)
        self.vb2.pack_start(self.combo,False,False,0)
        self._parent_.show_all()
        
    def refresh_gui(self):
        self.mainhbox.remove(self.vb1)
        self.vb1.destroy()
        self.mainhbox.remove(self.vb2)
        self.vb2.destroy()
        self._mainbox_.remove(self.mainhbox)
        self.mainhbox.destroy()
        self.gui()
        
    def on_combo_changed(self,combo):
        iter_ = self.combo.get_active_iter()
        if iter_ == None:
            return
        fntn=self.combo.get_model()[iter_][0]
        if fntn == "None":
            font.remove_config()
        else:
            check = font.set_config(fntn)
            fn = font.get_config()
            if fn :
                pangofont = Pango.font_description_from_string(fn)
                self.label.modify_font(pangofont)

    def on_addfontbutton_clicked(self,button):
        ffc=font.FolderFontsChooser(self._parent_)
        s=ffc.start()
        if s:
            font.CopyFonts(location=s,parent=self._parent_,spinner=self.spinner,refresh_fuction=self.refresh_gui).start()
        ffc.destroy()
