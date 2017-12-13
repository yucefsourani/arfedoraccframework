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
import imp
from arfedoraccframework.appinformation import appname, homedata


def search_and_load_plugins():
    """Searches the plugins folders and imports all valid plugins"""
    depl = []
    plugins_folders = [l for l in [homedata+"/plugins","/usr/share/{}/plugins".format(appname)] if os.path.isdir(l)]
    for plugin_folder in plugins_folders:
        for root, dirs, files in os.walk(plugin_folder):
            for module_file in files:
                if module_file.endswith(".py"):
                    if module_file not in depl:
                        module_name, module_extension = os.path.splitext(module_file)
                        try:
                            module_hdl, plugin_path_name, description = imp.find_module(os.path.join(root,module_name))
                            plugin = imp.load_module(os.path.join(root,module_name), module_hdl, plugin_path_name,description)
                            depl.append(module_file)
                        except Exception as e :
                            print(e)
                            print("Load {} Fail.".format(os.path.join(root,module_name)))
                            return False
                        finally:
                            if module_hdl:
                                module_hdl.close()
    
    return plugin
    
def get_plugins(ignore=None):
    """Searches the plugins folders"""
    depl = []
    result = []
    plugins_folders = [l for l in [homedata+"/plugins","/usr/share/{}/plugins".format(appname)] if os.path.isdir(l)]
    if ignore:
        for plugin_folder in plugins_folders:
            for root, dirs, files in os.walk(plugin_folder):
                for module_file in files:
                    if module_file.endswith(".py"):
                        if module_file not in depl:
                            if not root.split("/")[-1] in ignore:
                                module_name, module_extension = os.path.splitext(module_file)
                                result.append(os.path.join(root,module_name))
                                depl.append(module_file)
    else:
        for plugin_folder in plugins_folders:
            for root, dirs, files in os.walk(plugin_folder):
                for module_file in files:
                    if module_file.endswith(".py"):
                        if module_file not in depl:
                            module_name, module_extension = os.path.splitext(module_file)
                            result.append(os.path.join(root,module_name))
                            depl.append(module_file)

    
    return result

def load_plugin(module_name):
    """import valid plugin"""
    try:
        module_hdl, plugin_path_name, description = imp.find_module(module_name)
        plugin = imp.load_module(module_name, module_hdl, plugin_path_name,description)
    except Exception as e :
        print(e)
        print("Load {} Fail.".format(os.path.join(module_name+".py")))
        return False
    finally:
        if module_hdl:
            module_hdl.close()
    
    return plugin
    
if __name__ == "__main__":
    all_plugins=get_plugins()
    for module_name in all_plugins:
        print(load_plugin(module_name))
