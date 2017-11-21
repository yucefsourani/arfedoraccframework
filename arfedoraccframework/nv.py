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
import subprocess
import os
from bs4 import BeautifulSoup
import urllib
from arfedoraccframework.appinformation import homedata

filen = ""
filedrive_340 = ""
filedrive_304 = ""
filedrive_375 = ""
filedrive_384 = ""

def INIT():
	dlocation = os.path.join(homedata,"data")
	os.makedirs(dlocation,exist_ok=True)
	global filen
	global filedrive_340
	global filedrive_304
	global filedrive_375
	global filedrive_384
	filen = dlocation+"/pci.ids"
	filedrive_340 = dlocation+"/filedrive_340.ids"
	filedrive_304 = dlocation+"/filedrive_304.ids"
	filedrive_375 = dlocation+"/filedrive_375.ids"
	filedrive_384 = dlocation+"/filedrive_384.ids"



def get_drive_384(agent="Mozilla/5.0"):
    INIT()
    link = "http://us.download.nvidia.com/XFree86/Linux-x86_64/384.98/README/supportedchips.html"
    try:
        url = urllib.request.Request(link,headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(url)
        data = opurl.read().decode("utf-8")
        with open(filedrive_384,"w") as mf:
            mf.write(data)
    except Exception as e :
        print(e)
        return False
    opurl.close()
    return True

def drive_384(agent="Mozilla/5.0"):
    INIT()
    if not os.path.isfile(filedrive_384):
        check = get_drive_384(agent=agent)
        if not check:
            return False
				
    result = []
    try:
        opurl = open(filedrive_384)
        soup = BeautifulSoup(opurl,"html.parser")
        for tr in soup.findAll("tr"):
            try:
                result.append(tr.attrs["id"][2:])
            except:
                continue
    except Exception as e:
        print(e)
        return False
		
    opurl.close()
    return result
	
	

def get_drive_375(agent="Mozilla/5.0"):
    INIT()
    link = "http://us.download.nvidia.com/XFree86/Linux-x86_64/375.66/README/supportedchips.html"
    try:
        url = urllib.request.Request(link,headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(url)
        data = opurl.read().decode("utf-8")
        with open(filedrive_375,"w") as mf:
            mf.write(data)
    except Exception as e:
        print(e)
        return False
    opurl.close()
    return True

def drive_375(agent="Mozilla/5.0"):
    INIT()
    if not os.path.isfile(filedrive_375):
        check = get_drive_375(agent=agent)
        if not check:
            return False
				
    result = []
    try:
        opurl = open(filedrive_375)
        soup = BeautifulSoup(opurl,"html.parser")
        for tr in soup.findAll("tr"):
            try:
                result.append(tr.attrs["id"][2:])
            except:
                continue
    except Exception as e:
        print(e)
        return False
		
    opurl.close()
    return result
	

def get_drive_340(agent="Mozilla/5.0"):
    INIT()
    link = "http://us.download.nvidia.com/XFree86/Linux-x86_64/340.102/README/supportedchips.html"
    try:
        url = urllib.request.Request(link,headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(url)
        data = opurl.read().decode("utf-8")
        with open(filedrive_340,"w") as mf:
            mf.write(data)
    except Exception as e:
        print(e)
        return False
    opurl.close()
    return True

def drive_340(agent="Mozilla/5.0"):
    INIT()
    if not os.path.isfile(filedrive_340):
        check = get_drive_340(agent=agent)
        if not check:
            return False
				
    result = []
    try:
        opurl = open(filedrive_340)
        soup = BeautifulSoup(opurl,"html.parser")
        for tr in soup.findAll("tr"):
            try:
                result.append(tr.attrs["id"][2:])
            except:
                continue
    except Exception as e:
        print(e)
        return False
		
    opurl.close()
    return result



def get_drive_304(agent="Mozilla/5.0"):
    INIT()
    link = "http://us.download.nvidia.com/XFree86/Linux-x86_64/304.135/README/supportedchips.html"
    try:
        url = urllib.request.Request(link,headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(url)
        data = opurl.read().decode("utf-8")
        with open(filedrive_304,"w") as mf:
            mf.write(data)
    except Exception as e:
        print(e)
        return False
    return True

def drive_304(agent="Mozilla/5.0"):
    INIT()
    if not os.path.isfile(filedrive_304):
        check = get_drive_304(agent=agent)  
        if not check:
            return False
				
    result = []
    try:
        opurl = open(filedrive_304)
        soup = BeautifulSoup(opurl,"html.parser")
        for tr in soup.findAll("tr"):
            try:
                result.append(tr.attrs["id"][2:])
            except:
                continue
    except Exception as e:
        print(e)
        return False
		
    opurl.close()
    return result
	
def update_pciids(agent="Mozilla/5.0"):
    INIT()
    link  = "http://pciids.sourceforge.net/pci.ids"
    try:
        url   = urllib.request.Request(link,headers={"User-Agent":agent})
        opurl = urllib.request.urlopen(link)
        data  = opurl.read().decode("utf-8")
        with open(filen,"w") as mf:
            mf.write(data)
    except Exception as e:
        print(e)
        return False
    opurl.close()
    return True


def isdual():
    out=subprocess.Popen("lspci -nn | egrep -i \"3d|display|vga\"",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate()[0]
    if len([i for i in out.decode("utf-8").split("\n") if i])==2:
        return True
    return False
	

def get_ides_from_lspci(id_="10de"):
    lspci = subprocess.Popen(["lspci", "-n"], stdout=subprocess.PIPE).communicate()[0].decode("utf-8").split("\n")
    lspci = [i.split()[2].split(":")[1].lower() for i in lspci if i if i.split()[2].split(":")[0].lower()==id_]
    lspci.append("10D8".lower())
    return lspci

def found_in_pci_ids(id_="10de"):
    INIT()
    if not os.path.isfile(filen):
        check = update_pciids()
        if not check :
            return False
			
    b = False
    result = {}
    with open(filen) as mf:
        for line in mf:
            line = line.rstrip()
            if line.startswith(id_):
                b = True
                continue
            elif b and not line.startswith("\t") :
                if not line.startswith("#"):
                    b = False
                
            if b :
                if not line.startswith("\t\t") and line.startswith("\t"):
                    linestripsplit = line.lstrip().split(" ",1)
                    result.setdefault(linestripsplit[0],linestripsplit[1])
    return result


def get_nvidia_driver_name(d304,d340,d375,d384):
    result = {}
    drivers = {"akmod-nvidia-304xx" : d304,
			   "akmod-nvidia-340xx" : d340,
			   "akmod-nvidia-375xx" : d375,
			   "akmod-nvidia-384xx" : d384
			   }
    all_pci_ids = found_in_pci_ids("10de")
    if not all_pci_ids:
        return False
    all_nvidiacard = get_ides_from_lspci("10de")
    if not all_nvidiacard:
        return False
	
    for nvidiacard in all_nvidiacard:
        if nvidiacard in all_pci_ids.keys():
            if nvidiacard in drivers["akmod-nvidia-340xx"]:
                result.setdefault(all_pci_ids[nvidiacard],[nvidiacard,"akmod-nvidia-340xx xorg-x11-drv-nvidia-340xx kernel kernel-devel"])
            elif nvidiacard in drivers["akmod-nvidia-304xx"]:
                result.setdefault(all_pci_ids[nvidiacard],[nvidiacard,"akmod-nvidia-304xx xorg-x11-drv-nvidia-304xx kernel kernel-devel)"])
            #elif nvidiacard in drivers["akmod-nvidia-375xx"]:
             #   result.setdefault(all_pci_ids[nvidiacard],[nvidiacard,"akmod-nvidia-375xx xorg-x11-drv-nvidia-375xx kernel kernel-devel"])
            #elif nvidiacard in drivers["akmod-nvidia-384xx"]:
              #  result.setdefault(all_pci_ids[nvidiacard],[nvidiacard,"akmod-nvidia-384xx xorg-x11-drv-nvidia-384xx kernel kernel-devel"])
				
    return result


def issucureboot():
    out = subprocess.Popen("mokutil --sb-state",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8").strip()
    print(out)
    if out == "SecureBoot enabled":
        return True
    else:
        return False

    


