#
# Conditional build:
%bcond_with	gtk2		# build with gtk+2 (default is gtk+3)
%bcond_without	xfce		# Xfce 4 selector
#
Summary:	Desktop Input Method configuration tool
Summary(pl.UTF-8):	Narzędzie do konfiguracji metod wprowadzania znaków dla środowiska graficznego
Name:		im-chooser
Version:	1.6.4
Release:	4
License:	GPL v2
Group:		Applications
Source0:	http://fedorahosted.org/releases/i/m/im-chooser/%{name}-%{version}.tar.bz2
# Source0-md5:	fbf6598df98c9992e91aa62b7d33bc1b
Patch0:		%{name}-imchooserui.patch
Patch1:		%{name}-format.patch
URL:		http://fedorahosted.org/im-chooser/
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	imsettings-devel >= 1.3.0
%{?with_xfce:BuildRequires:	libxfce4util-devel}
BuildRequires:	xorg-lib-libSM-devel
%if %{with gtk2}
BuildRequires:	gtk+2-devel >= 2:2.16.0
BuildConflicts:	gtk+3-devel
%else
BuildRequires:	gtk+3-devel >= 3.0.0
#BuildRequires:	gnome-control-center-devel >= 3.0.0
%endif
Requires:	imsettings >= 1.3.0
Obsoletes:	im-chooser-gnome3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

%description -l pl.UTF-8
im-chooser to graficzne narzędzie do konfiguracji pozwalające na
wybór metody wprowadzania znaków (Input Method) lub wyłączenie
użycia IM w środowisku graficznym.

%package xfce
Summary:	im-chooser application for Xfce 4
Summary(pl.UTF-8):	Aplikacja im-chooser dla Xfce 4
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}

%description xfce
im-chooser is a GUI configuration tool to choose the Input Method
to be used or disable Input Method usage on the desktop.

This package contains the Xfce 4 application.

%description xfce -l pl.UTF-8
im-chooser to graficzne narzędzie do konfiguracji pozwalające na
wybór metody wprowadzania znaków (Input Method) lub wyłączenie
użycia IM w środowisku graficznym.

Ten pakiet zawiera aplikację przeznaczoną dla Xfce 4.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%configure \
	--disable-silent-rules \
	--disable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libimchooseui.{so,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/im-chooser
%attr(755,root,root) %{_libdir}/libimchooseui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libimchooseui.so.0
%{_datadir}/imchooseui
%{_desktopdir}/im-chooser.desktop
%{_iconsdir}/hicolor/*/apps/im-chooser.png
%{_mandir}/man1/im-chooser.1*

%if %{with xfce}
%files xfce
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xfce4-im-chooser
%{_desktopdir}/xfce4-im-chooser.desktop
%endif
