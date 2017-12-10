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
import dbus
dbus_service_name = "org.github.yucefsourani.ArfedoraControlCenter"
dbus_service_path = "/org/github/yucefsourani/ArfedoraControlCenter"
import slip.dbus.polkit as polkit

class RunRoot (object):
    def __init__ (self, bus):
        self.bus = bus
        self.dbus_service_path = "/".join ((dbus_service_path, "Backend"))
        self.dbus_object = bus.get_object (dbus_service_name, self.dbus_service_path)
        self.dbus_interface = dbus.Interface (self.dbus_object, dbus_service_name+".Backend")
        

    def call(self,a,timeout=1000000):
        try:
            check =  self.dbus_interface.call(a,timeout=timeout)
        except:
            return 1
        return check
    
    def callf(self,a,timeout=1000000):
        try:
            check =  self.dbus_interface.callf(a,timeout=timeout)
        except:
            return 1
        return check

    def Popen(self,a,timeout=1000000):
        try:
            out,err = self.dbus_interface.Popen(a,timeout=timeout)
        except:
            return ["","error"]
        return [out,err]

    def Popenf(self,a,timeout=1000000):
        try:
            out,err = self.dbus_interface.Popenf(a,timeout=timeout)
        except:
            return ["","error"]
        return [out,err]
        
    def Version(self):
        try:
            version =  self.dbus_interface.Version()
        except:
            return ""
        return version

runinroot=RunRoot(dbus.SystemBus())




