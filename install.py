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
import os
import site
import subprocess
import sys
import platform
from arfedoraccframework.appinformation import appname, homedata, icon_


arch=platform.machine()
if os.path.isfile("/usr/bin/apt"):
    tocheck =  ["/usr/lib/"]
else:
    tocheck = ["/usr/lib64/", "/usr/lib/"]
site_packages = [l for l in site.getsitepackages() for i in tocheck if l.startswith(i)][0]
if os.getuid()!=0:
    os.makedirs(homedata,exist_ok=True)
    subprocess.call("cp -r plugins {}".format(homedata),shell=True)
    subprocess.call("cp -r icons {}".format(homedata),shell=True)
else:
    os.makedirs("/usr/share/"+appname,exist_ok=True)
    subprocess.call("cp -r plugins /usr/share/"+appname,shell=True)
    subprocess.call("cp -r icons /usr/share/"+appname,shell=True)
subprocess.call("sudo cp {} {}".format(os.path.basename(icon_),icon_),shell=True)
subprocess.call("sudo cp -r arfedoraccframework {}".format(site_packages),shell=True)
subprocess.call("chmod 755  arfedoracontrolcenter",shell=True)
subprocess.call("sudo cp -r arfedoracontrolcenter /usr/bin/arfedoracontrolcenter",shell=True)
subprocess.call("sudo chmod 755  /usr/bin/arfedoracontrolcenter",shell=True)
to_translate = ["plugins/"+plugin for plugin in os.listdir("plugins") if plugin.endswith(".py")]
to_translate.append(appname)
to_translate =" ".join(to_translate)
subprocess.call("xgettext  --language=Python --keyword=_  -d {} -o po/{}.pot {}".format(appname,appname,to_translate),shell=True)

ts = ["po/"+f for f in os.listdir("po") if  os.path.isfile("po/"+f) and f.endswith(".po")]
copytolocale = []
for p in ts:
    mo = p[0:-3]+".mo"
    subprocess.call(" msgfmt -o {}  {}".format(mo,p),shell=True)
    target = "/usr/share/locale/"+os.path.basename(mo)[0:-3]+"/LC_MESSAGES/{}.mo".format(appname)
    copytolocale.append([mo,target])
for i in copytolocale:
    subprocess.call("sudo cp {} {}".format(i[0],i[1]),shell=True)

