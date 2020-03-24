%global appname arfedoracontrolcenter
Name:           arfedora-control-center
Version:        3.3
Release:        6%{?dist}
Summary:        ArFedora control Center
Group:		Applications/System
BuildArch:	noarch
License:        GPLv3
URL:            https://arfedora.blogspot.com
Source0:        https://github.com/yucefsourani/arfedoraccframework/archive/master.zip
BuildRequires:	gettext
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-devel
Requires:	python3
Requires:	python3-gobject
#Requires:	pygobject3
Requires:	python3-dbus
Requires:	python3-dnf
Requires:	udisks2
Requires:	polkit
Requires:	ntfsprogs
Requires:	parted
Requires:	dosfstools
Requires:	python3-beautifulsoup4
Requires:	mokutil
Requires:	python3-slip-dbus
Requires:	fontconfig

%description
ArFedora control Center.




%prep
%autosetup -n arfedoraccframework-master
msgfmt -o %{appname}.mo po/ar.po
rm plugins/gnome_tweak_themes_v2.0.py






%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{python3_sitelib}
mkdir -p %{buildroot}%{_datadir}/%{appname}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/locale/ar/LC_MESSAGES
mkdir -p %{buildroot}%{_libexecdir}/arfedoracontrolcenter
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions
mkdir -p %{buildroot}%{_datadir}/dbus-1/system-services


install -pDm0755 %{appname} %{buildroot}%{_bindir}/%{appname}
cp -r arfedoraccframework %{buildroot}%{python3_sitelib}/arfedoraccframework
cp -r icons %{buildroot}%{_datadir}/%{appname}/icons
cp -r plugins %{buildroot}%{_datadir}/%{appname}/plugins
cp  %{appname}.mo %{buildroot}%{_datadir}/locale/ar/LC_MESSAGES/%{appname}.mo
cp com.github.yucefsourani.ArControlCenter.desktop  %{buildroot}%{_datadir}/applications/com.github.yucefsourani.ArControlCenter.desktop
cp org.github.yucefsourani.ArControlCenter.png %{buildroot}%{_datadir}/pixmaps/org.github.yucefsourani.ArControlCenter.png
install -pDm0755 pk/arfedoracontrolcenter_dbus_service.py %{buildroot}%{_libexecdir}/arfedoracontrolcenter/arfedoracontrolcenter_dbus_service.py
cp pk/org.github.yucefsourani.ArfedoraControlCenter.conf %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.github.yucefsourani.ArfedoraControlCenter.conf
cp pk/org.github.yucefsourani.ArfedoraControlCenter.policy %{buildroot}%{_datadir}/polkit-1/actions/org.github.yucefsourani.ArfedoraControlCenter.policy
cp pk/org.github.yucefsourani.ArfedoraControlCenter.service %{buildroot}%{_datadir}/dbus-1/system-services/org.github.yucefsourani.ArfedoraControlCenter.service


%files
%license  LICENSE
%doc README.md
%{_bindir}/%{appname}
%{python3_sitelib}/arfedoraccframework/*
%{_datadir}/%{appname}/icons/*
%{_datadir}/%{appname}/plugins/*
%{_datadir}/locale/ar/LC_MESSAGES/%{appname}.mo
%{_datadir}/applications/com.github.yucefsourani.ArControlCenter.desktop
%{_datadir}/pixmaps/org.github.yucefsourani.ArControlCenter.png
%{_libexecdir}
%{_sysconfdir}/dbus-1/system.d/org.github.yucefsourani.ArfedoraControlCenter.conf
%{_datadir}/polkit-1/actions/org.github.yucefsourani.ArfedoraControlCenter.policy
%{_datadir}/dbus-1/system-services/org.github.yucefsourani.ArfedoraControlCenter.service



%changelog
* Thu Mar 24 2020 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-6
- Release 6 

* Sat Apr 01 2019 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-5
- Release 5 

* Sat Apr 01 2019 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-4
- Release 4 

* Sat Apr 01 2019 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-3
- Release 3 

* Fri Feb 01 2019 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-2
- Release 2 

* Fri Feb 01 2019 yucuf sourani <youssef.m.sourani@gmail.com> 3.3-1
- Version 3.3 

* Sat Sep 29 2018 yucuf sourani <youssef.m.sourani@gmail.com> 3.0-2
- Release 2 

* Sat Sep 22 2018 youcef sourani <youssef.m.sourani@gmail.com> - 3.0-1
- Version 3.0

* Thu Sep 20 2018 youcef sourani <youssef.m.sourani@gmail.com> - 2.9-1
- Release 2

* Wed May 02 2018 youcef sourani <youssef.m.sourani@gmail.com> - 2.8-2
- Release 2


* Sun Apr 08 2018 youcef sourani <youssef.m.sourani@gmail.com> - 2.8-1
- Update To v2.8

* Thu Dec 21 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.7-1
- Update To v2.7

* Thu Dec 21 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.6-1
- Update To v2.6

* Wed Dec 20 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.5-1
- Update To v2.5

* Wed Dec 13 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.4-1
- Update To v2.4

* Wed Dec 13 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.3-1
- Update To v2.3

* Wed Dec 13 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.2-1
- Update To v2.2

* Wed Dec 13 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.1-1
- Update To v2.1

* Mon Dec 11 2017 youcef sourani <youssef.m.sourani@gmail.com> - 2.0-1
- Update To v2.0

* Mon Dec 04 2017 youcef sourani <youssef.m.sourani@gmail.com> - 1.2-1
- Update To v1.2

* Fri Dec 01 2017 youcef sourani <youssef.m.sourani@gmail.com> - 1.1-2
- Update To v1.1

* Fri Dec 01 2017 youcef sourani <youssef.m.sourani@gmail.com> - 1.0-3
- Release 3
- Remove gnome-shell-extension-EasyScreenCast

* Fri Nov 17 2017 yucef sourani <youssef.m.sourani@gmail.com> - 1.0-2
- Release 2

* Fri Nov 17 2017 yucef sourani <youssef.m.sourani@gmail.com> - 1.0-1
- Initial for fedora 27


