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
from os.path import basename,join
import time
import subprocess
import dbus
import string


class Patition(object):
    def __init__(self,bus,block_device):
        self.__bus           = bus
        self.block_device    = block_device
        self.__proxy         = self.__bus.get_object("org.freedesktop.UDisks2",self.block_device)
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.DBus.Properties")
        self.NAME            = "/dev/"+basename(self.block_device)
        self.SIZE            = self.__interface.Get("org.freedesktop.UDisks2.Block","Size")
        self.TYPE            = self.__interface.Get("org.freedesktop.UDisks2.Block","IdType")
        self.SELF            = self
        
        self.__umount_interface = dbus.Interface(self.__proxy,"org.freedesktop.UDisks2.Filesystem")
        self.__umount = self.__umount_interface.get_dbus_method("Unmount")
            
    def umount_(self,force):
        try:
            self.__umount({"force" : force})
        except Exception as e :
            print(e)
            return False

class Drive(object):
    def __init__(self,bus,block_device):
        self.__bus           = bus
        self.__block_device  = block_device
        self.__proxy         = self.__bus.get_object("org.freedesktop.UDisks2",self.__block_device)
        self.__interface     = dbus.Interface(self.__proxy,"org.freedesktop.DBus.Properties")
        self.ALLPATTIONS     = self.__all_parttions()
        
    def __all_parttions(self):
        result = []
        p = self.__interface.Get("org.freedesktop.UDisks2.PartitionTable","Partitions")
        for i in p:
            try:
                result.append(Patition(self.__bus,i))
            except:
                pass
        return result

        

def INIT():
    bus = dbus.SystemBus()
    result  = []
    for char in string.ascii_lowercase :
        try:
            bus.get_object("org.freedesktop.UDisks2","/org/freedesktop/UDisks2/block_devices/sd{}".format(char))
            result.append(Drive(bus,"/org/freedesktop/UDisks2/block_devices/sd{}".format(char)))
        except :
            pass
    return result
    
    



def lsof_(location):
	check = subprocess.check_output("lsof {}".format(location).split())
	return check.decode("utf-8")
	
def get_parttions_by_type(type_):
    bus = dbus.SystemBus()
    result = dict()
    for d in INIT():
        for i in d.ALLPATTIONS:
            if "all" in type_:
                result.setdefault(i.NAME,[i.SELF,i.SIZE,i.TYPE])
            elif i.TYPE in type_:
                result.setdefault(i.NAME,[i.SELF,i.SIZE,i.TYPE])
    return result



