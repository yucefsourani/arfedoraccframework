#!/usr/bin/python3
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
from gi.repository import GLib
from bs4 import BeautifulSoup
import os

def get_fonts(lang=False,_format='%{family}\n'):
    family = repr(_format)
    if lang :
        out,err = subprocess.Popen("fc-list -f {} :lang={}".format(family,lang),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
    else:
        out,err = subprocess.Popen("fc-list -f "+family,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        print("fc-list "+family)
    if out:
        return out.decode("utf-8")
    else:
        return False

def get_fonts_name(lang=False):
    result = []
    _fonts =  get_fonts(lang=lang)
    _fonts = [i for i in _fonts.split("\n")]
    return [i.split(",")[-1] for i in _fonts if i]



#files   = [GLib.get_home_dir()+"/.fonts.conf", GLib.get_user_config_dir()+"/fontconfig/fonts.conf"]
#folders = [GLib.get_home_dir()+"/.fonts.conf.d", GLib.get_user_config_dir()+"/fontconfig/conf.d"]

def set_config(fontname):
    config = """<fontconfig>
<!-- Default font for the ar locale (no fc-match pattern) -->
<match>
<test compare="contains" name="lang">
<string>ar</string>
</test>
<edit mode="prepend" name="family">
<string>__NAME__</string>
</edit>
</match>
<dir>~/.fonts</dir>
</fontconfig>
"""
    configfile = GLib.get_user_config_dir()+"/fontconfig/conf.d/99-arfedora-fonts-config.conf"
    try:
        with open(configfile,"w") as mf:
            mf.write(config.replace("__NAME__",fontname))
    except:
        return False
    return True
    
def get_config():
    configfile = GLib.get_user_config_dir()+"/fontconfig/conf.d/99-arfedora-fonts-config.conf"
    if not os.path.isfile(configfile):
        return False
    try:
        with open(configfile) as mf:
            soup     = BeautifulSoup(mf,"xml")
            fontname = soup.find("match").find("edit").find("string").text
    except:
        return False
    return fontname

def remove_config():
    subprocess.call("rm "+GLib.get_user_config_dir()+"/fontconfig/conf.d/99-arfedora-fonts-config.conf",shell=True)
