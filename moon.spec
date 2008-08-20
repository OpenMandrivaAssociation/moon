%define name moon
%define version 0.8
%define release %mkrel 1
%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Summary: Open Source implementation of Silverlight
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.bz2
Patch: moon-0.8-expat.patch
Patch1: moon-0.7-fix-linking.patch
License: LGPLv2
Group: System/Libraries
Url: http://www.mono-project.com/Moonlight
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: ffmpeg-devel
BuildRequires: libxtst-devel
BuildRequires: libxrandr-devel
%if %mdvver >= 200900
BuildRequires: libcairo-devel >= 1.6
BuildRequires: xulrunner-devel-unstable
%else
BuildRequires: libmozilla-firefox-devel
%endif
BuildRequires: libgtk+2.0-devel
BuildRequires: libmagick-devel
BuildRequires: dbus-glib-devel
BuildRequires: libalsa-devel
BuildRequires: mono-devel
BuildRequires: ndesk-dbus gnome-desktop-sharp-devel

%description
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.

%package -n %libname
Group:System/Libraries
Summary: Open Source implementation of Silverlight

%description -n %libname
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.

%package -n %develname
Group:Development/C++
Summary: Open Source implementation of Silverlight
Requires: %libname = %version-%release
Provides: lib%name-devel = %version-%release

%description -n %develname
Moonlight is an open source implementation of Microsoft Silverlight
for Unix systems. It supports rich browser applications, similar to
Adobe Flash.


%prep
%setup -q
%patch -p1
%patch1 -p1 -b .fix-linking
aclocal -I pixman -I cairo
autoconf
automake

%build
#export CPPFLAGS="-I%_includedir/libswscale"
#--with-swscale=yes \

#gw tests don't build
%define _disable_ld_no_undefined 1
%configure2_5x \
%if %mdvver < 200900
--with-ff2=yes \
%else
  --with-ff3=yes \
  --with-cairo=system \
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std 
mkdir -p %buildroot%_libdir/mozilla/plugins
mv %buildroot%_libdir/moon/plugin/libmoonloader* %buildroot%_libdir/mozilla/plugins
rm -f %buildroot%_libdir/moon/plugin/README

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README TODO
%_bindir/agviewer
%_bindir/mopen1
%_libdir/moon
%_libdir/mozilla/plugins/libmoon*
#gw TODO: put somewhere else
%_libdir/libshocker.so

%files -n %libname
%defattr(-,root,root)
%_libdir/libmoon.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/libmoon.so
%_libdir/*.la
%_libdir/pkgconfig/moon.pc
%_includedir/libmoon

