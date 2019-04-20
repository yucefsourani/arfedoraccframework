#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  selinux_v1.0.py
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
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk,Gio,GObject
from arfedoraccframework.baseplugin import BasePlugin
from arfedoraccframework.baseutils import get_icon_location
    
button_label         = _("AutoStart Manager")
button_image         = ["appointment-soon"]
category             = _("System")
title                = _("AutoStart Manager")
arch                 = ["all"]
distro_name          = ["all"]
distro_version       = ["all"]
mainbuttontooltip    = _("AutoStart Manager")
blockclose           = False
if_true_skip         = False
if_false_skip        = True
if_one_true_skip     = [False]
if_all_true_skip     = [False]
priority             = 0
category_icon_theme  = "applications-system"

class Yes_Or_No(Gtk.MessageDialog):
    def __init__(self,msg,parent=None):
        Gtk.MessageDialog.__init__(self,buttons = Gtk.ButtonsType.OK_CANCEL)
        self.props.message_type = Gtk.MessageType.QUESTION
        self.props.text         = msg
        self.p=parent
        if self.p != None:
            self.parent=self.p
            self.set_transient_for(self.p)
            self.set_modal(True)
            self.p.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)
            
    def check(self):
        rrun = self.run()
        if rrun == Gtk.ResponseType.OK:
            self.destroy()
            if self.p != None:
                self.p.set_sensitive(True)
            return True
        else:
            if self.p != None:
                self.p.set_sensitive(True)
            self.destroy()
        return False

class NInfo(Gtk.MessageDialog):
    def __init__(self,message,parent=None):
        Gtk.MessageDialog.__init__(self,parent,1,Gtk.MessageType.INFO,Gtk.ButtonsType.OK,message)
        self.props.use_markup=True
        self.parent=parent
        if self.parent != None:
            self.set_transient_for(self.parent)
            self.set_modal(True)
            self.parent.set_sensitive(False)
        else:
            self.set_position(Gtk.WindowPosition.CENTER)

        self.get_message_area().get_children()[0].set_selectable(True)
        
    def start(self):
        self.run() 
        if self.parent != None:
            self.parent.set_sensitive(True)
        self.destroy()
        return False



class AddApp(Gtk.Window):
    __gsignals__ = { 
                "cancel" : (GObject.SignalFlags.RUN_LAST,GObject.TYPE_NONE,()),
                "apply"  : (GObject.SignalFlags.RUN_LAST,GObject.TYPE_NONE,(GObject.TYPE_STRING,GObject.TYPE_STRING)),
                "error"  : (GObject.SignalFlags.RUN_LAST,GObject.TYPE_NONE,())
                
    }
    def __init__(self,parent=None):
        Gtk.Window.__init__(self)
        self.__header = Gtk.HeaderBar()
        self.set_titlebar(self.__header)
        self.connect("delete-event",self.__on_delete_event)
        self.parent = parent 
        self.set_transient_for(self.parent)
        self.set_modal(True)
        self.__name    = ""
        self.__comment = ""
        self.__exec    = ""
        
    def start(self):
        mainbox = Gtk.VBox()
        mainbox.props.spacing = 20
        h  = Gtk.HBox()
        h.props.spacing = 10
        v1 = Gtk.VBox()
        v1.props.spacing = 5
        v2 = Gtk.VBox()
        v2.props.spacing = 5
        for k in ["Name","Comment","Command"] :
            l = Gtk.Label()
            l.props.label = k
            e = Gtk.Entry()
            e.connect("notify::text",self.__on_entry_text_notify,k)
            
            v1.pack_start(l,True,True,0)
            v2.pack_start(e,True,True,0)         
        
        buttonbox     = Gtk.HBox()
        apply_buuton  = Gtk.Button.new_with_mnemonic("_Apply")
        apply_buuton.connect("clicked",self.__on_apply)
        cancel_buuton = Gtk.Button.new_with_mnemonic("_Cancel")
        cancel_buuton.connect("clicked",self.__on_cancel)
        buttonbox.pack_start(cancel_buuton,True,True,0)
        buttonbox.pack_start(apply_buuton,True,True,0)
        
        h.pack_start(v1,True,True,0)
        h.pack_start(v2,True,True,0)
        mainbox.pack_start(h,True,True,0)
        mainbox.pack_start(buttonbox,True,True,0)
        self.add(mainbox)
        self.show_all()

    def __on_apply(self,button):
        if not all([self.__name,self.__comment,self.__exec]):
            self.emit("error")
        else:
            tmp = """[Desktop Entry]
Encoding=UTF-8
Name={}
GenericName={}
Comment={}
Exec={}
Terminal=false
Type=Application
Categories=GTK;
StartupNotify=false
""".format(self.__name,self.__name,self.__comment,self.__exec)
            self.emit("apply",tmp,self.__name)
        self.destroy()
        
    def __on_cancel(self,button):
        self.emit("cancel")
        self.destroy()
        
    def __on_delete_event(self,window,event):
        self.emit("cancel")
        self.destroy()

    def __on_entry_text_notify(self,entry,t,k):
        if k=="Name":
            self.__name = entry.props.text
        elif k=="Comment":
            self.__comment = entry.props.text
        elif k=="Command":
            self.__exec = entry.props.text

class AutoStart(Gtk.Bin):
    def __init__(self,parent):
        Gtk.Bin.__init__(self)
        self.autostart_files_locations = [os.path.expanduser("~/.config/autostart")]
        self.parent = parent

    def run(self):
        listbox  = Gtk.ListBox.new()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hboxmain = Gtk.HBox()

        v1       = Gtk.VBox()
        v1.props.spacing = 20
        v2       = Gtk.VBox()
        v2.props.spacing = 20
        for f in self.get_all_autostart(self.autostart_files_locations):
            h         = Gtk.HBox()
            h.props.spacing = 10
            file_icon = f.get_icon()
            name      = f.get_name()
            filename  = f.get_filename()
            
            if file_icon:
                icon = Gtk.Image.new_from_gicon(file_icon,Gtk.IconSize.DIALOG  )
                h.pack_start(icon,False,False,0)
            
            label   = Gtk.Label()
            label.props.label = name
            h.pack_start(label,False,False,0)
            
            bdelete = Gtk.HBox()
            delete  = Gtk.Button()
            delete.props.label = "Delete"
            delete.connect("clicked",self.on_delete_clicked,f,v1,v2,h,bdelete)
            bdelete.pack_start(delete,True,False,0)
            
            v1.pack_start(h,True,True,0)
            v2.pack_start(bdelete,True,True,0)

        
        hboxmain.pack_start(v1,True,True,0)
        hboxmain.pack_start(v2,False,True,0)
        

        addbutton = Gtk.Button()
        addbutton.props.label = "Select App"
        addbutton.connect("clicked",self.__on_add_button_clicked,v1,v2)
        
        addbutton2 = Gtk.Button()
        addbutton2.props.label = "Custom App"
        addbutton2.connect("clicked",self.__on_add_button_clicked2,v1,v2)
        
        listbox.add(hboxmain)
        listbox.add(addbutton)
        listbox.add(addbutton2)
        self.add(listbox)
        self.show_all()
        
    def __on_add_button_clicked2(self,button,v1,v2):
        addapp    = AddApp(self.parent)
        addapp.connect("apply",self.__on_add_app_apply,v1,v2)
        addapp.start()

    def __on_add_button_clicked(self,button,v1,v2):
        appc = Gtk.AppChooserDialog.new_for_content_type(self.parent,Gtk.DialogFlags(1),"*")
        w = appc.get_widget()
        w.set_default_text("Select Application")
        w.set_show_all(True)
        w.set_show_default(False)
        w.set_show_fallback(False)
        w.set_show_other(False)
        w.set_show_recommended(False)
        content   = appc.get_content_area ()
        content.get_children()[1].get_children()[-1].destroy()
        content.get_children()[1].get_children()[-1].destroy()
        #appc.get_header_bar().set_subtitle("Select Application")
        
        run = appc.run()
        if run==Gtk.ResponseType.OK:
            app_ = appc.get_app_info()
            appc.destroy()
            self.__on_app_chooser_re(app_,v1,v2)
            return 
        appc.destroy()

    def __on_app_chooser_re(self,app,v1,v2):
        source = app.get_filename()
        target = os.path.expanduser("~/.config/autostart/{}".format(os.path.basename(source)))
        if subprocess.call("cp {} {}".format(source,target),shell=True)!=0:
            n = NInfo("'cp {} {}' Failed.".format(source,target),self.parent)
            n.start()
            return False
        try:
            f = Gio.DesktopAppInfo.new_from_filename(target)
            h         = Gtk.HBox()
            h.props.spacing = 10
            file_icon = f.get_icon()
            name      = f.get_name()
            filename  = f.get_filename()
            
            if file_icon:
                icon = Gtk.Image.new_from_gicon(file_icon,Gtk.IconSize.DIALOG  )
                h.pack_start(icon,False,False,0)
            
            label   = Gtk.Label()
            label.props.label = name
            h.pack_start(label,False,False,0)
            
            bdelete = Gtk.HBox()
            delete  = Gtk.Button()
            delete.props.label = "Delete"
            delete.connect("clicked",self.on_delete_clicked,f,v1,v2,h,bdelete)
            bdelete.pack_start(delete,True,False,0)
            
            v1.pack_start(h,True,True,0)
            v2.pack_start(bdelete,True,True,0)
            v1.show_all()
            v2.show_all()
        except Exception as e:
            try:
                os.remove(target)
            except:
                pass
            n = NInfo(e,self.parent)
            n.start()
            return False
        
        return True
        
    def __on_add_app_apply(self,addapp,result,name,v1,v2):
        file_location = os.path.expanduser("~/.config/autostart/{}".format(name.strip()+".desktop"))
        try:
            with open(file_location,"w") as myfile:
                myfile.write(result)
        except Exception as e:
            n = NInfo(e,self.parent)
            n.start()
            return False
        try:
            f = Gio.DesktopAppInfo.new_from_filename(file_location)
            h         = Gtk.HBox()
            h.props.spacing = 10
            file_icon = f.get_icon()
            name      = f.get_name()
            filename  = f.get_filename()
            
            if file_icon:
                icon = Gtk.Image.new_from_gicon(file_icon,Gtk.IconSize.DIALOG  )
                h.pack_start(icon,False,False,0)
            
            label   = Gtk.Label()
            label.props.label = name
            h.pack_start(label,False,False,0)
            
            bdelete = Gtk.HBox()
            delete  = Gtk.Button()
            delete.props.label = "Delete"
            delete.connect("clicked",self.on_delete_clicked,f,v1,v2,h,bdelete)
            bdelete.pack_start(delete,True,False,0)
            
            v1.pack_start(h,True,True,0)
            v2.pack_start(bdelete,True,True,0)
            v1.show_all()
            v2.show_all()
        except Exception as e:
            try:
                os.remove(file_location)
            except:
                pass
            n = NInfo(e,self.parent)
            n.start()
            return False
        
        return True
        
    def on_delete_clicked(self,button,file_,v1,v2,h,bdelete):
        filename = file_.get_filename()
        check = Yes_Or_No("Are You Sure You Want To Delete\n{} ?".format(filename),self.parent)
        if not check.check():
            return 
        if file_.delete():
            v1.remove(h)
            v2.remove(bdelete)
            h.destroy()
            bdelete.destroy()
        else:
            n = NInfo("Delete {} Failed.".format(file_.get),self.parent)
            n.start()
            
            
    def get_all_autostart(self,locations):
        result = []
        for l in locations:
            try:
                if os.path.isdir(l):
                    for base,folders,files in os.walk(l):
                        for f in files:
                            f = os.path.join(base,f)
                            if os.path.isfile(f):
                                try:
                                    de = Gio.DesktopAppInfo.new_from_filename(f)
                                    result.append(de)
                                except :
                                    continue
            except Exception as e:
                print(e)
                continue
        return result


class Plugin(BasePlugin):
    def __init__(self,parent,boxparent):
        BasePlugin.__init__(self,parent=parent,boxparent=boxparent)
        self.gui()
        
    def gui(self):
        self._mainbox_.set_border_width(5)
        label  = Gtk.Label()
        label.props.label = _("AutoStart Manager")
        self._mainbox_.pack_start(label,True,True,0)
        autostart = AutoStart(self._parent_)
        self._mainbox_.pack_start(autostart,True,True,0)
        autostart.run()            
        self._parent_.show_all()
        
