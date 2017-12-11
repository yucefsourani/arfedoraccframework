#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gnometweaktool_control_center_v1.0.py
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
import subprocess


desktop=os.getenv("XDG_CURRENT_DESKTOP")
if os.path.isfile("/usr/bin/gnome-tweak-tool") and "GNOME" in desktop:
    desktop = "GNOMETWEAKTOOL"

button_label         = _("Gnome Tweak Tool")
button_image         = "gnome_tweak_tool_22409.png"
category             = _("System")
title                = _("For Test")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("Gnome Tweak Tool")
blockclose           = False
if_true_skip         = False
if_false_skip        = True if "GNOMETWEAKTOOL" in desktop else False
if_one_true_skip     = [False]
if_all_true_skip     = [True,False]
priority             = 3
category_icon_theme  = "applications-system" 

def Run(button):
    subprocess.Popen("/usr/bin/gnome-tweak-tool",shell=True)

