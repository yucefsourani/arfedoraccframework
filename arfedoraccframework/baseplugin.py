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
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk


class BasePlugin(object):
    def __init__(self,parent,boxparent,destroy=True):
        self._mainbox_   = Gtk.VBox()
        self._parent_    = parent
        self._boxparent_ = boxparent
        self.__destroy   = destroy
        
    def run(self):
        self._boxparent_.add(self._mainbox_)
    
    def stop(self):
        self._boxparent_.remove(self._mainbox_)
        if self.__destroy:
            self._mainbox_.destroy()


