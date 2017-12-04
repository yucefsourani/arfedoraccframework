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
from bs4 import BeautifulSoup
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GLib
import os
from shutil import copy2
import threading

class  CopyFonts(threading.Thread):
    def __init__(self,location,parent,spinner,refresh_fuction=None):
        threading.Thread.__init__(self)
        self.location        = location
        self.parent          = parent
        self.spinner         = spinner
        self.refresh_fuction = refresh_fuction
        
    def run(self):
        GLib.idle_add(self.parent.set_sensitive,False)
        GLib.idle_add(self.spinner.start)
        done = False
        fonts_folder = GLib.get_user_data_dir()+"/fonts"
        os.makedirs(fonts_folder,exist_ok=True)
        for dirname,folders,files in os.walk(self.location):
            for file_ in files:
                if file_.lower().endswith("ttf") or file_.lower().endswith("otf") or file_.lower().endswith("fon"):
                    file_ = os.path.join(dirname,file_)
                    try:
                        copy2(file_,fonts_folder)
                        done = True
                    except Exception as e:
                        print(e)
                        GLib.idle_add(self.parent.set_sensitive,True)
                        return False
        if done:
            subprocess.call("chmod 755 -R {}/*".format(fonts_folder),shell=True)
            subprocess.call("fc-cache -fv",shell=True)
        GLib.idle_add(self.spinner.stop)
        GLib.idle_add(self.parent.set_sensitive,True)
        if done:
            if self.refresh_fuction:
                GLib.idle_add(self.refresh_fuction)
        return True

                
            

class FolderFontsChooser(Gtk.FileChooserDialog):
    def __init__(self,parent):
        Gtk.FileChooserDialog.__init__(self,parent=parent,action=Gtk.FileChooserAction.SELECT_FOLDER)
        self.set_title("FileChooserDialog")
        self.add_button("_Open", Gtk.ResponseType.OK)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        self.set_default_response(Gtk.ResponseType.OK)

        

    def start(self):
        response = self.run()
        if response == Gtk.ResponseType.OK:
            return self.get_filename()
        else:
            return False
        
        
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
    os.makedirs(GLib.get_user_config_dir()+"/fontconfig/conf.d",exist_ok=True)
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
