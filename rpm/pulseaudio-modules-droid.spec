%define pulseversion %{expand:%(rpm -q --qf '[%%{version}]' pulseaudio)}
%define pulsemajorminor %{expand:%(echo '%{pulseversion}' | cut -d+ -f1)}
%define moduleversion %{pulsemajorminor}.%{expand:%(echo '%{version}' | cut -d. -f3)}

Name:       pulseaudio-modules-droid

Summary:    PulseAudio Droid HAL modules
Version:    %{pulsemajorminor}.79
Release:    1
Group:      Multimedia/PulseAudio
License:    LGPLv2+
URL:        https://github.com/mer-hybris/pulseaudio-modules-droid
Source0:    %{name}-%{version}.tar.bz2
Requires:   pulseaudio >= %{pulseversion}
Requires:   %{name}-common = %{version}-%{release}
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libtool-ltdl-devel
BuildRequires:  pkgconfig(pulsecore) >= %{pulsemajorminor}
BuildRequires:  pkgconfig(android-headers)
BuildRequires:  pkgconfig(libhardware)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(expat)

%description
PulseAudio Droid HAL modules.

%package common
Summary:    Common libs for the PulseAudio droid modules
Requires:   pulseaudio >= %{pulseversion}

%description common
This contains common libs for the PulseAudio droid modules.

%package devel
Summary:    Development files for PulseAudio droid modules
Group:      Development/Libraries
Requires:   %{name}-common = %{version}-%{release}
Requires:   pulseaudio >= %{pulseversion}

%description devel
This contains development files for PulseAudio droid modules.

%prep
%setup -q -n %{name}-%{version}

%build
echo "%{moduleversion}" > .tarball-version
# Obtain the DEVICE from the same source as used in /etc/os-release
. /usr/lib/droid-devel/hw-release.vars
%reconfigure --disable-static --with-droid-device=$MER_HA_DEVICE
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%files
%defattr(-,root,root,-)
%{_libdir}/pulse-%{pulsemajorminor}/modules/libdroid-sink.so
%{_libdir}/pulse-%{pulsemajorminor}/modules/libdroid-source.so
%{_libdir}/pulse-%{pulsemajorminor}/modules/module-droid-sink.so
%{_libdir}/pulse-%{pulsemajorminor}/modules/module-droid-source.so
%{_libdir}/pulse-%{pulsemajorminor}/modules/module-droid-card.so
%{_libdir}/pulse-%{pulsemajorminor}/modules/module-droid-keepalive.so
%license COPYING

%files common
%defattr(-,root,root,-)
%{_libdir}/pulse-%{pulsemajorminor}/modules/libdroid-util.so

%files devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/pulsecore/modules/droid
%{_prefix}/include/pulsecore/modules/droid/version.h
%{_prefix}/include/pulsecore/modules/droid/conversion.h
%{_prefix}/include/pulsecore/modules/droid/droid-config.h
%{_prefix}/include/pulsecore/modules/droid/droid-util.h
%{_libdir}/pkgconfig/*.pc
