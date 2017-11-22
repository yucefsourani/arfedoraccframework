#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rpmfusion.py
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
from arfedoraccframework.runinroot import runinroot

packages_name = ["rpmfusion-nonfree-release-$(rpm -E %fedora)","rpmfusion-free-release-$(rpm -E %fedora)"]

def check_if_exists():
    for p in packages_name:
        if subprocess.call("rpm -q "+p,shell=True)!=0:
            return False
    return True    

def installrpmfusion():
    if not check_if_exists():
        return onlyinstallrpmfusion()
    return 0
    
def onlyinstallrpmfusion():
    return  runinroot.call("dnf install -y  --nogpgcheck --best http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm")

