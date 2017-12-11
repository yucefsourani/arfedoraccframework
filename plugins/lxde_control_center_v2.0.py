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
import subprocess
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location



button_label         = _("Lxde Control Center")
button_image         = "cropped-lxde-icon.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Lxde Control Center")
blockclose           = False
if_true_skip         = False
if_false_skip        = all([ os.path.isfile("/usr/bin/lxappearance") ,os.path.isfile("/usr/bin/lxsession-default-apps"),os.path.isfile("/usr/bin/lxsession-edit" ),os.path.isfile("/usr/bin/lxrandr"),os.path.isfile("/usr/bin/lxinput")])
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-system"


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        mainvbox = Gtk.VBox(spacing=20)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        lock_ = False
        """desktop=os.getenv("XDG_CURRENT_DESKTOP")
        if desktop=="":
            if os.getenv("DESKTOP_SESSION")=="/usr/share/xsessions/openbox":
                desktop = "OpenBox"
                
        desktop_cc={"GNOME"      :["Gnome Center",get_icon_location("gnome-logo-icon-23471.png"),"/usr/bin/gnome-control-center"],
                    "KDE"        :["Kde Control Center",get_icon_location("11949942481641741323about_kde.svg.hi.png"),"/usr/bin/systemsettings5"] ,
                    "XFCE"       :["Xfce Control Center",get_icon_location("XFCE-full.sh.png"),"/usr/bin/xfce4-settings-manager"] ,
                    "X-LXQt"     :["Lxqt Control Center",get_icon_location("lxqt_logo_by_i_sty-d7rmlxd.png"),"/usr/bin/lxqt-config"] ,
                    "X-Cinnamon" :["Cinnamon Center",get_icon_location("mintlogo-kde.svg"),"/usr/share/cinnamon/cinnamon-settings/cinnamon-settings.py"],
                    "MATE"       :["Mate Control Center",get_icon_location("mate_desktop_logo.jpg"),"/usr/bin/mate-control-center"] ,
                    "X-Hawaii"   :["Hawaii Control Center",get_icon_location("clip_art_illustration_of_a_beautiful_colorful_parrot_sitting_on_a_branch_the_background_has_a_rainbow_and_palm_trees_0515-1102-0914-3316_SMU.jpg"),"/usr/bin/hawaii-system-preferences"],
                    "Openbox"    :["Openbox Manager Configuration",get_icon_location("Openbox-logo.png"),"/usr/bin/obconf"]
                    } 
        
        for k_ in desktop_cc.keys():
            if False:#skiped
                lock_ = True
                self._mainbox_.set_border_width(100)
                hbox1 = Gtk.HBox(spacing=10)
                vbox1 = Gtk.VBox(spacing=20)
                op = desktop_cc[desktop]
                vheader = Gtk.VBox(spacing=3)
                vbox1.pack_start(vheader,False,False,0)
                label = Gtk.Label("<b>"+op[0]+"</b>",use_markup=True)
                label.set_line_wrap(True)
                label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                label.set_max_width_chars(13)
                label.set_justify(Gtk.Justification.CENTER)
                pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(op[1],100,100)
                image  = Gtk.Image.new_from_pixbuf(pixbuf)
                vheader.pack_start(image,False,False,0)
                vheader.pack_start(label,False,False,0)
                bbox = Gtk.HBox()
                button = Gtk.Button("Run")
                #button.get_style_context().add_class("destructive-action")
                button.set_size_request(150,40)
                button.connect("clicked",self.on_button_clicked,op[2])
                hseparator = Gtk.Separator()
                hseparator.set_margin_top(30)
                hseparator.set_margin_top(30)
                bbox.pack_start(button,True,False,0)
                vbox1.pack_start(bbox,False,False,0)
                if os.path.isfile("/usr/bin/gnome-tweak-tool") and "GNOME" in k_:
                    i = get_icon_location("gnome_tweak_tool_22409.png")
                    vbox2 = Gtk.VBox(spacing=20)
                    vheader2 = Gtk.VBox(spacing=3)
                    vbox2.pack_start(vheader2,False,False,0)
                    label2 = Gtk.Label("<b>Gnome Tweak Tool</b>",use_markup=True)
                    label2.set_line_wrap(True)
                    label2.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                    label2.set_max_width_chars(13)
                    pixbuf2=GdkPixbuf.Pixbuf.new_from_file_at_size(i,100,100)
                    image2  = Gtk.Image.new_from_pixbuf(pixbuf2)
                    vheader2.pack_start(image2,False,False,0)
                    vheader2.pack_start(label2,False,False,0)
                    bbox2 = Gtk.HBox()
                    button2 = Gtk.Button("Run")
                    #button2.get_style_context().add_class("destructive-action")
                    button2.set_size_request(150,40)
                    button2.connect("clicked",self.on_button_clicked,"/usr/bin/gnome-tweak-tool")
                    bbox2.pack_start(button2,True,False,0)
                    vbox2.pack_start(bbox2,False,False,0)
                
                hbox1.pack_start(vbox1,True,False,0)
                if os.path.isfile("/usr/bin/gnome-tweak-tool") and "GNOME" in k_:
                    hbox1.pack_start(hseparator,True,False,0)
                    hbox1.pack_start(vbox2,True,False,0)
                    mainvbox.pack_start(hbox1,False,False,0)
                else:
                    vseparator = Gtk.Separator()
                    vseparator.set_margin_top(10)
                    mainvbox.pack_start(hbox1,False,False,0)
                    mainvbox.pack_start(vseparator,False,False,0)"""
        
        if not lock_:
            self._mainbox_.set_border_width(5)
            lxde_cc=[ [_("Customize Look and Feel"),"/usr/bin/lxappearance"] ,[_("Default Applications"),"/usr/bin/lxsession-default-apps"],[_("Desktop Session Settings"),"/usr/bin/lxsession-edit"] ,[_("Display Settings"),"/usr/bin/lxrandr"],[_("Windows Manager Configuration"),"/usr/bin/obconf"],[_("Input Device Preferences"),"/usr/bin/lxinput"]]
            lxde_logo = get_icon_location("cropped-lxde-icon.png")
            hbox1 = Gtk.HBox(spacing=10)
            vbox1 = Gtk.VBox(spacing=20)
            vheader = Gtk.VBox(spacing=3)
            vbox1.pack_start(vheader,False,False,0)
            label = Gtk.Label(_("<b>Lxde Control Programs</b>"),use_markup=True)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
            label.set_max_width_chars(13)
            label.set_justify(Gtk.Justification.CENTER)
            pixbuf=GdkPixbuf.Pixbuf.new_from_file_at_size(lxde_logo,100,100)
            image  = Gtk.Image.new_from_pixbuf(pixbuf)
            vheader.pack_start(image,False,False,0)
            vheader.pack_start(label,False,False,0)
            for i in lxde_cc:
                if os.path.isfile(i[1]):
                    button = Gtk.Button(i[0])
                    #button.get_style_context().add_class("destructive-action")
                    button.set_size_request(150,40)
                    button.connect("clicked",self.on_button_clicked,i[1])
                    vbox1.pack_start(button,False,False,0)
            
            vseparator = Gtk.Separator()
            vseparator.set_margin_top(10)
            hbox1.pack_start(vbox1,True,False,0)
            mainvbox.pack_start(hbox1,False,False,0)
            mainvbox.pack_start(vseparator,False,False,0)
            
        
        

    def on_button_clicked(self,button,torun):
        subprocess.Popen(torun,shell=True)

