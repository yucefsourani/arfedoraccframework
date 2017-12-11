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
import dbus
import math
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,GdkPixbuf, Pango
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location





button_label         = _("Drives Info")
button_image         = "hdd.png"
category             = _("Utilities")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Drives Info")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 0
category_icon_theme  = "applications-utilities"



def get_all_devices():
	bus = dbus.SystemBus()
	result  = []
	object_   = bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2")
	for i in object_.get_dbus_method("GetManagedObjects","org.freedesktop.DBus.ObjectManager")():
		if i.startswith("/org/freedesktop/UDisks2/block_devices/") and i[39:-1]=="sd":
			ob        = bus.get_object("org.freedesktop.UDisks2",i)
			interface = dbus.Interface(ob,"org.freedesktop.DBus.Properties")
			drive=interface.Get("org.freedesktop.UDisks2.Block","Drive")
			result.append(["/dev/{}".format(i[39:]),drive])

	return result
	

 
def get_drives_info(drives):
	result = {}
	bus = dbus.SystemBus()
	for drive in drives:
		try:
			object_       = bus.get_object("org.freedesktop.UDisks2",drive[1])
			propos        = dbus.Interface(object_,"org.freedesktop.DBus.Properties")
			id_           = propos.Get("org.freedesktop.UDisks2.Drive","Id")
			model         = propos.Get("org.freedesktop.UDisks2.Drive","Model")
			size          = propos.Get("org.freedesktop.UDisks2.Drive","Size") /1024 /1024
			speed         = propos.Get("org.freedesktop.UDisks2.Drive","RotationRate")
			removable     = "True" if propos.Get("org.freedesktop.UDisks2.Drive","Removable") else "False"
			connectionbus = propos.Get("org.freedesktop.UDisks2.Drive","ConnectionBus")
			if not connectionbus:
				connectionbus = "None"
			logo_ = get_icon_location("eject-hard-disk_318-32032.jpg") if removable=="True"  else get_icon_location("hard-disk-outline_318-53576.jpg")

			dr_            = "Drive      "+drive[0]
			id__           = "Id      "+id_
			model_         = "Model      "+model
			size_          = "Size      "+str(round(size,2))+"MB"+" {}GB".format(math.ceil(size/1024))
			speed_         = "Speed      "+str(speed)
			removable_     = "Removable      "+removable
			connectionbus_ = "ConnectionBus      "+connectionbus
            
			result.setdefault(dr_,[logo_,dr_,id__,model_,size_,speed_,removable_,connectionbus_])
		except:
			pass
	return result
	
class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        mainvbox = Gtk.VBox(spacing=20)
        mainvbox.set_margin_left(90)
        mainvbox.set_margin_right(90)
        self._mainbox_.set_border_width(5)
        self._mainbox_.pack_start(mainvbox,False,False,0)
        headericon   = get_icon_location("hdd.png")
        headerbox    = Gtk.VBox(spacing=6)
        headerpixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(headericon,100,100)
        headerimage  = Gtk.Image.new_from_pixbuf(headerpixbuf)
        headerlabel  = Gtk.Label(_("<b>Drives Info</b>"),use_markup=True)
        headerlabel.set_line_wrap(True)
        headerlabel.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
        headerlabel.set_max_width_chars(13)
        headerlabel.set_justify(Gtk.Justification.CENTER)
        headerbox.pack_start(headerimage,False,False,0)
        headerbox.pack_start(headerlabel,False,False,0)
        headervseparator = Gtk.Separator()
        headervseparator.set_margin_bottom(30)
        hbox = Gtk.HBox(spacing=10)
        mainvbox.pack_start(headerbox,False,False,0)
        mainvbox.pack_start(headervseparator,False,False,0)
        mainvbox.pack_start(hbox,False,False,0)
        
        vb = Gtk.VBox(spacing=50)
        drives = get_drives_info(get_all_devices())
        for k,v in drives.items():
            h = Gtk.HBox(spacing=50)
            vblogo = Gtk.VBox(spacing=2)
            vbinfo1 = Gtk.VBox(spacing=2)
            h.pack_start(vblogo,False,False,0)
            h.pack_start(vbinfo1,False,False,0)
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(v[0],100,100)
            image  = Gtk.Image.new_from_pixbuf(pixbuf)
            vblogo.pack_start(image,False,False,0)
            
            for l in v[1:]:
                mainlb1 = Gtk.HBox()
                label1  = Gtk.Label(l,use_markup=True)
                label1.set_line_wrap(True)
                label1.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR )
                label1.set_justify(Gtk.Justification.CENTER)
                mainlb1.pack_start(label1,False,False,0)
                vbinfo1.pack_start(mainlb1,False,False,0)

            vb.pack_start(h,False,False,0)
        mainvbox.pack_start(vb,False,False,0)
            
        fvseparator = Gtk.Separator()
        fvseparator.set_margin_top(30)
        fvseparator.set_margin_bottom(30)
        mainvbox.pack_start(fvseparator,False,False,0)


			
        

