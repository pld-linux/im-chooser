#
# Conditional build:
%bcond_with	gtk2		# build with gtk+2 (default is gtk+3)
#
Summary:	Desktop Input Method configuration tool
#Summary(pl.UTF-8):	-
Name:		im-chooser
Version:	1.4.2
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://fedorahosted.org/releases/i/m/%{name}/%{name}-%{version}.tar.bz2
# Source0-md5:	f5205239f8d259ecd7720097346d440d
Patch0:		%{name}-enable-apps-on-gnome.patch
URL:		http://fedorahosted.org/im-chooser/
%if %{with gtk2}
BuildRequires:	gtk+2-devel
BuildConflicts:	gtk+3-devel
%else
BuildRequires:	gtk+3-devel
BuildRequires:	gnome-control-center-devel
%endif
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	imsettings-devel >= 1.2.0
BuildRequires:	desktop-file-utils
Requires:	imsettings >= 1.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

#%description -l pl.UTF-8

%package	gnome3
Summary:	control-center module for im-chooser on GNOME3
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description gnome3
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

This package contains the control-center panel module on GNOME3.

%prep
%setup -q
%patch0 -p1

%build
%configure \
	--with-desktopfile=%{_datadir}/applications/im-chooser.desktop

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{!?with_gtk2:%{__rm} $RPM_BUILD_ROOT%{_libdir}/control-center-1/panels/libim-chooser.{a,la}}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libimchooseui.{so,la,a}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor

%postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/im-chooser
%attr(755,root,root) %{_libdir}/libimchooseui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimchooseui.so.[0-9]
%{_desktopdir}/im-chooser.desktop
%{_desktopdir}/xfce4-im-chooser.desktop
%{_iconsdir}/hicolor/*/apps/im-chooser.png

%files gnome3
%defattr(644,root,root,755)
%{_libdir}/control-center-1/panels/libim-chooser.so
%{_desktopdir}/im-chooser-panel.desktop
