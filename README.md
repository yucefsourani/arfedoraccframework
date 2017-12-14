# arfedoraccframework
https://arfedora.blogspot.com

Python+Gtk Framework to make control center from plugins (tested on fedora only)


# Install On Fedora
  
sudo dnf copr enable youssefmsourani/arcontrolcenter -y
  
sudo dnf install arfedora-control-center -y



# Install On Other Distro

cd && git clone https://github.com/yucefsourani/arfedoraccframework

cd ~/arfedoraccframework

chmod 755 install.py

./install.py

arfedoracontrolcenter



# Screenshot

![Alt text](https://raw.githubusercontent.com/yucefsourani/arfedoraccframework/master/Screenshot%20from%202017-12-14%2003-38-16.jpg "Screenshot")
  
# وثائق
https://arfedora.blogspot.com/2017/11/arfedoracontrolcenter.html





* Requires

  * ``` python3 ```
  
  * ``` python3-dbus ```
  
  * ``` pygobject3 ```
 
  * ``` python3-gobject ```
  
  * ``` gettext #devel ```
  
  * ``` python3-slip-dbus ```
  
  * ``` polkit ```
  
  
  
  
  
* Plugins Requires

  * ``` python3-dnf (Fedora Only) ```
  
  * ``` udisks2 ```
 
  * ``` ntfsprogs ```
  
  * ``` parted ```
    
  * ``` dosfstools ```
  
  * ``` bash ```
  
  * ``` python3-beautifulsoup4 ```

  * ``` mokutil ```

  * ``` fontconfig ```





* Optional Requires For Gnome Tweak Themes Plugin (Fedora See https://copr.fedorainfracloud.org/coprs/youssefmsourani/arcontrolcenter/packages/ )
  * ``` breeze-cursor-theme ```
  
  * ``` anderson-wallpaper ```
  
  * ``` ant-themes ```
  
  * ``` gnome-shell-extension-clipboard-indicator ```
  
  * ``` gnome-shell-extension-CoverflowAltTab ```
  
  * ``` gnome-shell-extension-dash-to-dock ```
    
  * ``` gnome-shell-extension-EasyScreenCast ```
      
  * ``` gnome-shell-extension-simple-net-speed ```
 
  * ``` gnome-shell-extension-user-theme ```

  * ``` gnome-shell-extension-drive-menu ```

  * ``` macos-icon-theme ```
  
  


