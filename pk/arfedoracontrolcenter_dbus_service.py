#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  dbus_service.py
#  
#  Copyright 2017 youcefsourani <youcef@fedora.youcef>
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

import os.path
import sys
import dbus.service
import slip.dbus.service
import slip.dbus.polkit as polkit
from gi.repository import GObject
import dbus.mainloop.glib
import subprocess


dbus_service_name = "org.github.yucefsourani.ArfedoraControlCenter"
dbus_service_path = "/org/github/yucefsourani/ArfedoraControlCenter"

class Backend (slip.dbus.service.Object):
    default_polkit_auth_required = "org.github.yucefsourani.ArfedoraControlCenter.Call"
    def __init__ (self, bus_name, object_path):
        slip.dbus.service.Object.__init__ (self, bus_name, object_path)
        print ("*** Serivce __init__: Running ArfedoraControlCenter dbus service at '{}'.".format(dbus_service_name))


    @polkit.require_auth("org.github.yucefsourani.ArfedoraControlCenter.Call")
    @dbus.service.method(dbus_interface = dbus_service_name + ".Backend",in_signature="s", out_signature="i")   
    def call(self,args):
        return subprocess.call(args,shell=True)

    @polkit.require_auth("org.github.yucefsourani.ArfedoraControlCenter.Call")
    @dbus.service.method(dbus_interface = dbus_service_name + ".Backend",in_signature="s", out_signature="i")   
    def callf(self,args):
        return subprocess.call(args.split())


    @polkit.require_auth("org.github.yucefsourani.ArfedoraControlCenter.Call")
    @dbus.service.method(dbus_interface = dbus_service_name + ".Backend",in_signature="s", out_signature="as")   
    def Popen(self,args):
        out,err = subprocess.Popen(args,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        return [out.decode("utf-8"),err.decode("utf-8")]
        
    @polkit.require_auth("org.github.yucefsourani.ArfedoraControlCenter.Call")
    @dbus.service.method(dbus_interface = dbus_service_name + ".Backend",in_signature="s", out_signature="as")   
    def Popenf(self,args):
        out,err = subprocess.Popen(args.split(),shell=False,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()
        return [out.decode("utf-8"),err.decode("utf-8")]
                
    @dbus.service.method(dbus_interface = dbus_service_name + ".Backend")    
    def Version(self):
        return "2.0"
        

        
def run_service ():
    mainloop = GObject.MainLoop ()
    dbus.mainloop.glib.DBusGMainLoop (set_as_default=True)
    system_bus = dbus.SystemBus ()
    name = dbus.service.BusName (dbus_service_name, system_bus)
    backend = Backend (name, dbus_service_path + "/Backend")
    slip.dbus.service.set_mainloop (mainloop)
    print ("*** Running ArfedoraControlCenter dbus service at '%s'." % (dbus_service_name))
    mainloop.run ()



if __name__ == "__main__":
    run_service ()
