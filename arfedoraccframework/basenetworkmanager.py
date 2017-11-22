#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  basenetwrokmanager.py
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


class NetworkManager(object):
    def __init__(self):
        self.__bus              = dbus.SystemBus()
        self.__name             = "org.freedesktop.NetworkManager"
        __objectpath            =  "/org/freedesktop/NetworkManager"
        __object_               = self.__bus.get_object(self.__name,__objectpath)
        self.__propertiesi      = dbus.Interface(__object_,"org.freedesktop.DBus.Properties")
        self.__methodi          = dbus.Interface(__object_,"org.freedesktop.NetworkManager")
        
        
    def getPropertie(self,interface,propertie):
        return self.__propertiesi.Get(interface,propertie)

    def getMethod(self,method):
        return self.__methodi
        
    def getAllInterfaceNAME(self):
        result = []
        devices = self.getPropertie("org.freedesktop.NetworkManager","AllDevices")
        for device in devices:
            object_      = self.__bus.get_object(self.__name,device)
            propertiesi  = dbus.Interface(object_,"org.freedesktop.DBus.Properties")
            result.append(propertiesi.Get("org.freedesktop.NetworkManager.Device","Interface"))
        return result
        
    def getAllWirelessInterfaceNAME(self):
        result = []
        for interface in self.getAllInterfaceNAME():
            if interface.startswith("wl"):
                result.append(interface)
        return result


