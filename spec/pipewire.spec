%global majorversion 0
%global minorversion 3
%global microversion 51

%global apiversion   0.3
%global spaversion   0.2
%global soversion    0
%global libversion   %{soversion}.%(bash -c '((intversion = (%{minorversion} * 100) + %{microversion})); echo ${intversion}').0

# For rpmdev-bumpspec and releng automation
%global baserelease 2

%global snapdate  202206030856
%global gitcommit 87172fde061438bef6a8cafe83ad7ad70007c7d2
%global shortcommit %(c=%{gitcommit}; echo ${c:0:7})

# https://bugzilla.redhat.com/983606
%global _hardened_build 1

# where/how to apply multilib hacks
%global multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 ppc64le

# Build conditions for various features
%bcond_without alsa
%bcond_without vulkan

# Features disabled for RHEL 8
%if 0%{?rhel} && 0%{?rhel} < 9
%bcond_with pulse
%bcond_with jack
%else
%bcond_without pulse
%bcond_without jack
%endif

# Features disabled for RHEL
%if 0%{?rhel}
%bcond_with jackserver_plugin
%else
%bcond_without jackserver_plugin
%endif

# Disabled for RHEL < 10 and Fedora < 36
%if (0%{?rhel} && 0%{?rhel} < 10) || (0%{?fedora} && 0%{?fedora} < 36)
%bcond_with libcamera_plugin
%else
%bcond_without libcamera_plugin
%endif

%bcond_without v4l2

Name:           pipewire
Summary:        Media Sharing Server
Version:        %{majorversion}.%{minorversion}.%{microversion}
Release:        %{?snapdate:%{snapdate}git%{shortcommit}}%{?dist}
License:        MIT
URL:            https://pipewire.org/
%if 0%{?snapdate}
Source0:        https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{gitcommit}/pipewire-%{shortcommit}.tar.gz
%else
Source0:        https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/pipewire-%{version}.tar.gz
%endif

## upstream patches

## upstreamable patches

## fedora patches

BuildRequires:  gettext
BuildRequires:  meson >= 0.49.0
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0) >= 2.32
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.32
BuildRequires:  pkgconfig(gstreamer-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-net-1.0) >= 1.10.0
BuildRequires:  pkgconfig(gstreamer-allocators-1.0) >= 1.10.0
# libldac is not built on x390x, see rhbz#1677491
%ifnarch s390x
BuildRequires:  pkgconfig(ldacBT-enc)
BuildRequires:  pkgconfig(ldacBT-abr)
%endif
BuildRequires:  pkgconfig(fdk-aac)
%if %{with vulkan}
BuildRequires:  pkgconfig(vulkan)
%endif
BuildRequires:  pkgconfig(bluez)
BuildRequires:  systemd-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libv4l-devel
BuildRequires:  doxygen
BuildRequires:  python-docutils
BuildRequires:  graphviz
BuildRequires:  sbc-devel
BuildRequires:  libsndfile-devel
BuildRequires:  ncurses-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  avahi-devel
BuildRequires:  pkgconfig(webrtc-audio-processing) >= 0.2
BuildRequires:  libusb1-devel
BuildRequires:  readline-devel
BuildRequires:  lilv-devel
BuildRequires:  openssl-devel
BuildRequires:  libcanberra-devel

Requires(pre):  shadow-utils
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       systemd
Requires:       rtkit
# A virtual Provides so we can swap session managers
Requires:       pipewire-session-manager
# Prefer WirePlumber for session manager
Suggests:       wireplumber

%description
PipeWire is a multimedia server for Linux and other Unix like operating
systems.

%package libs
Summary:        Libraries for PipeWire clients
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{name}-libpulse < %{version}-%{release}

%description libs
This package contains the runtime libraries for any application that wishes
to interface with a PipeWire media server.

%package gstreamer
Summary:        GStreamer elements for PipeWire
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description gstreamer
This package contains GStreamer elements to interface with a
PipeWire media server.

%package devel
Summary:        Headers and libraries for PipeWire client development
License:        MIT
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Headers and libraries for developing applications that can communicate with
a PipeWire media server.

%package doc
Summary:        PipeWire media server documentation
License:        MIT

%description doc
This package contains documentation for the PipeWire media server.

%package utils
Summary:        PipeWire media server utilities
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
This package contains command line utilities for the PipeWire media server.

%if %{with alsa}
%package alsa
Summary:        PipeWire media server ALSA support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%if ! (0%{?fedora} && 0%{?fedora} < 34)
# Ensure this is provided by default to route all audio
Supplements:    %{name} = %{version}-%{release}
# Replace PulseAudio and JACK ALSA plugins with PipeWire
## N.B.: If alsa-plugins gets updated in F33, this will need to be bumped
Obsoletes:      alsa-plugins-jack < 1.2.2-5
Obsoletes:      alsa-plugins-pulseaudio < 1.2.2-5
%endif

%description alsa
This package contains an ALSA plugin for the PipeWire media server.
%endif

%if %{with jack}
%package jack-audio-connection-kit
Summary:        PipeWire JACK implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Conflicts:      jack-audio-connection-kit
Conflicts:      jack-audio-connection-kit-dbus
# Fixed jack subpackages
Conflicts:      %{name}-libjack < 0.3.13-6
Conflicts:      %{name}-jack-audio-connection-kit < 0.3.13-6
# Replaces libjack subpackage
Obsoletes:      %{name}-libjack < 0.3.19-2
Provides:       %{name}-libjack = %{version}-%{release}
Provides:       %{name}-libjack%{?_isa} = %{version}-%{release}
%if ! (0%{?fedora} && 0%{?fedora} < 34)
# Ensure this is provided by default to route all audio
Supplements:    %{name} = %{version}-%{release}
# Replace JACK with PipeWire-JACK
## N.B.: If jack gets updated in F33, this will need to be bumped
Obsoletes:      jack-audio-connection-kit < 1.9.16-2
%endif

%description jack-audio-connection-kit
This package provides a JACK implementation based on PipeWire

%package jack-audio-connection-kit-devel
Summary:        Development files for %{name}-jack-audio-connection-kit
License:        MIT
Requires:       %{name}-jack-audio-connection-kit%{?_isa} = %{version}-%{release}
Conflicts:      jack-audio-connection-kit-devel
Enhances:       %{name}-jack-audio-connection-kit

%description jack-audio-connection-kit-devel
This package provides development files for building JACK applications
using PipeWire's JACK library.
%endif

%if %{with jackserver_plugin}
%package plugin-jack
Summary:        PipeWire media server JACK support
License:        MIT
BuildRequires:  jack-audio-connection-kit-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       jack-audio-connection-kit

%description plugin-jack
This package contains the PipeWire spa plugin to connect to a JACK server.
%endif

%if %{with libcamera_plugin}
%package plugin-libcamera
Summary:        PipeWire media server libcamera support
License:        MIT
BuildRequires:  libcamera-devel
BuildRequires:  libdrm-devel
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libcamera
Requires:       libdrm

%description plugin-libcamera
This package contains the PipeWire spa plugin to access cameras through libcamera.
%endif

%if %{with pulse}
%package pulseaudio
Summary:        PipeWire PulseAudio implementation
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:  pulseaudio-libs
Conflicts:      pulseaudio
# Fixed pulseaudio subpackages
Conflicts:      %{name}-libpulse < 0.3.13-6
Conflicts:      %{name}-pulseaudio < 0.3.13-6
%if ! (0%{?fedora} && 0%{?fedora} < 34)
# Ensure this is provided by default to route all audio
Supplements:    %{name} = %{version}-%{release}
# Replace PulseAudio with PipeWire-PulseAudio
## N.B.: If pulseaudio gets updated in F33, this will need to be bumped
Obsoletes:      pulseaudio < 14.2-3
Obsoletes:      pulseaudio-esound-compat < 14.2-3
Obsoletes:      pulseaudio-module-bluetooth < 14.2-3
Obsoletes:      pulseaudio-module-gconf < 14.2-3
Obsoletes:      pulseaudio-module-gsettings < 14.2-3
Obsoletes:      pulseaudio-module-jack < 14.2-3
Obsoletes:      pulseaudio-module-lirc < 14.2-3
Obsoletes:      pulseaudio-module-x11 < 14.2-3
Obsoletes:      pulseaudio-module-zeroconf < 14.2-3
Obsoletes:      pulseaudio-qpaeq < 14.2-3
%endif

# Virtual Provides to support swapping between PipeWire-PA and PA
Provides:       pulseaudio-daemon
Conflicts:      pulseaudio-daemon
Provides:       pulseaudio-module-bluetooth
Provides:       pulseaudio-module-jack

%description pulseaudio
This package provides a PulseAudio implementation based on PipeWire
%endif

%if %{with v4l2}
%package v4l2
Summary:        PipeWire media server v4l2 LD_PRELOAD support
License:        MIT
Recommends:     %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description v4l2
This package contains an LD_PRELOAD library that redirects v4l2 applications to
PipeWire.
%endif

%prep
%autosetup -p1 %{?snapdate:-n %{name}-%{gitcommit}}

%build
%meson \
    -D docs=enabled -D man=enabled -D gstreamer=enabled -D systemd=enabled	\
    -D gstreamer-device-provider=disabled -D sdl2=disabled 			\
    -D audiotestsrc=disabled -D videotestsrc=disabled				\
    -D volume=disabled -D bluez5-codec-aptx=disabled -D roc=disabled 		\
%ifarch s390x
    -D bluez5-codec-ldac=disabled						\
%endif
    -Dbluez5-codec-lc3plus=disabled						\
    -D session-managers=[] 				\
    %{!?with_jack:-D pipewire-jack=disabled} 					\
    %{!?with_jackserver_plugin:-D jack=disabled} 				\
    %{!?with_libcamera_plugin:-D libcamera=disabled} 				\
    %{?with_jack:-D jack-devel=true} 					\
    %{!?with_alsa:-D pipewire-alsa=disabled}					\
    %{?with_vulkan:-D vulkan=enabled}
%meson_build

%install
%meson_install

%if %{with jack}
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo %{_libdir}/pipewire-%{apiversion}/jack/ > %{buildroot}%{_sysconfdir}/ld.so.conf.d/pipewire-jack-%{_arch}.conf
%else
rm %{buildroot}%{_datadir}/pipewire/jack.conf

%endif

%if %{with alsa}
mkdir -p %{buildroot}%{_sysconfdir}/alsa/conf.d/
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/50-pipewire.conf
cp %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf \
        %{buildroot}%{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf

%endif

%if ! %{with pulse}
# If the PulseAudio replacement isn't being offered, delete the files
rm %{buildroot}%{_bindir}/pipewire-pulse
rm %{buildroot}%{_userunitdir}/pipewire-pulse.*
rm %{buildroot}%{_datadir}/pipewire/pipewire-pulse.conf

%endif

%find_lang %{name}

# upstream should use udev.pc
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
mv -fv %{buildroot}/lib/udev/rules.d/90-pipewire-alsa.rules %{buildroot}%{_prefix}/lib/udev/rules.d


%check
%ifarch s390x
# FIXME: s390x FAIL: pw-test-stream, pw-test-endpoint
%global tests_nonfatal 1
%endif
%meson_test || TESTS_ERROR=$?
if [ "${TESTS_ERROR}" != "" ]; then
echo "test failed"
%{!?tests_nonfatal:exit $TESTS_ERROR}
fi

%pre
getent group pipewire >/dev/null || groupadd -r pipewire
getent passwd pipewire >/dev/null || \
    useradd -r -g pipewire -d %{_localstatedir}/run/pipewire -s /sbin/nologin -c "PipeWire System Daemon" pipewire
exit 0

%post
%systemd_user_post pipewire.service
%systemd_user_post pipewire.socket

%triggerun -- %{name} < 0.3.6-2
# This is for upgrades from previous versions which had a static symlink.
# The %%post scriptlet above only does anything on initial package installation.
# Remove before F33.
systemctl --no-reload preset --global pipewire.socket >/dev/null 2>&1 || :

%if %{with pulse}
%post pulseaudio
%systemd_user_post pipewire-pulse.service
%systemd_user_post pipewire-pulse.socket
%endif

%files
%license LICENSE COPYING
%doc README.md
%{_userunitdir}/pipewire.*
%{_bindir}/pipewire
%{_mandir}/man1/pipewire.1*
%{_mandir}/man1/pipewire-pulse.1*
%dir %{_datadir}/pipewire/
%{_datadir}/pipewire/pipewire.conf
%{_datadir}/pipewire/minimal.conf
%{_datadir}/pipewire/filter-chain/*.conf
%{_mandir}/man5/pipewire.conf.5*

%files libs -f %{name}.lang
%license LICENSE COPYING
%doc README.md
%{_libdir}/libpipewire-%{apiversion}.so.*
%{_libdir}/pipewire-%{apiversion}/libpipewire-*.so
%dir %{_datadir}/alsa-card-profile/
%dir %{_datadir}/alsa-card-profile/mixer/
%{_datadir}/alsa-card-profile/mixer/paths/
%{_datadir}/alsa-card-profile/mixer/profile-sets/
%dir %{_datadir}/spa-0.2/
%{_datadir}/spa-0.2/bluez5/bluez-hardware.conf
%{_prefix}/lib/udev/rules.d/90-pipewire-alsa.rules
%dir %{_libdir}/spa-%{spaversion}
%{_libdir}/spa-%{spaversion}/alsa/
%{_libdir}/spa-%{spaversion}/aec/
%{_libdir}/spa-%{spaversion}/audioconvert/
%{_libdir}/spa-%{spaversion}/audiomixer/
%{_libdir}/spa-%{spaversion}/bluez5/
%{_libdir}/spa-%{spaversion}/control/
%{_libdir}/spa-%{spaversion}/support/
%{_libdir}/spa-%{spaversion}/v4l2/
%{_libdir}/spa-%{spaversion}/videoconvert/
%if %{with vulkan}
%{_libdir}/spa-%{spaversion}/vulkan/
%endif
%{_datadir}/pipewire/client.conf
%{_datadir}/pipewire/client-rt.conf

%files gstreamer
%{_libdir}/gstreamer-1.0/libgstpipewire.*

%files devel
%{_libdir}/libpipewire-%{apiversion}.so
%{_includedir}/pipewire-%{apiversion}/
%{_includedir}/spa-%{spaversion}/
%{_libdir}/pkgconfig/libpipewire-%{apiversion}.pc
%{_libdir}/pkgconfig/libspa-%{spaversion}.pc

%files doc
%{_datadir}/doc/pipewire/html

%files utils
%{_bindir}/pw-mon
%{_bindir}/pw-metadata
%{_bindir}/pw-dsdplay
%{_bindir}/pw-mididump
%{_bindir}/pw-midiplay
%{_bindir}/pw-midirecord
%{_bindir}/pw-cli
%{_bindir}/pw-dot
%{_bindir}/pw-cat
%{_bindir}/pw-dump
%{_bindir}/pw-link
%{_bindir}/pw-loopback
%{_bindir}/pw-play
%{_bindir}/pw-profiler
%{_bindir}/pw-record
%{_bindir}/pw-reserve
%{_bindir}/pw-top
%{_mandir}/man1/pw-mon.1*
%{_mandir}/man1/pw-cli.1*
%{_mandir}/man1/pw-cat.1*
%{_mandir}/man1/pw-dot.1*
%{_mandir}/man1/pw-link.1*
%{_mandir}/man1/pw-metadata.1*
%{_mandir}/man1/pw-mididump.1*
%{_mandir}/man1/pw-profiler.1*
%{_mandir}/man1/pw-top.1*

%{_bindir}/spa-acp-tool
%{_bindir}/spa-inspect
%{_bindir}/spa-json-dump
%{_bindir}/spa-monitor
%{_bindir}/spa-resample

%if %{with alsa}
%files alsa
%{_libdir}/alsa-lib/libasound_module_pcm_pipewire.so
%{_libdir}/alsa-lib/libasound_module_ctl_pipewire.so
%{_datadir}/alsa/alsa.conf.d/50-pipewire.conf
%{_datadir}/alsa/alsa.conf.d/99-pipewire-default.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/50-pipewire.conf
%config(noreplace) %{_sysconfdir}/alsa/conf.d/99-pipewire-default.conf
%endif

%if %{with jack}
%files jack-audio-connection-kit
%{_bindir}/pw-jack
%{_mandir}/man1/pw-jack.1*
%{_libdir}/pipewire-%{apiversion}/jack/libjack.so.*
%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so.*
%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so.*
%{_datadir}/pipewire/jack.conf
%{_sysconfdir}/ld.so.conf.d/pipewire-jack-%{_arch}.conf

%files jack-audio-connection-kit-devel
%{_includedir}/jack/
%{_libdir}/pipewire-%{apiversion}/jack/libjack.so
%{_libdir}/pipewire-%{apiversion}/jack/libjacknet.so
%{_libdir}/pipewire-%{apiversion}/jack/libjackserver.so
%{_libdir}/pkgconfig/jack.pc
%endif

%if %{with jackserver_plugin}
%files plugin-jack
%{_libdir}/spa-%{spaversion}/jack/
%endif

%if %{with libcamera_plugin}
%files plugin-libcamera
%{_libdir}/spa-%{spaversion}/libcamera/
%endif

%if %{with pulse}
%files pulseaudio
%{_bindir}/pipewire-pulse
%{_userunitdir}/pipewire-pulse.*
%{_datadir}/pipewire/pipewire-pulse.conf
%endif

%if %{with v4l2}
%files v4l2
%{_bindir}/pw-v4l2
%{_libdir}/pipewire-%{apiversion}/v4l2/libpw-v4l2.so
%endif

%changelog
* Thu May 05 2022 Peter Hutterer <peter.hutterer@redhat.com>
- Disable lc3plus, not available in fedora

* Wed Feb 16 2022 Peter Hutterer <peter.hutterer@redhat.com>
- Add spa aec dir

* Tue Dec 14 2021 Peter Hutterer <peter.hutterer@redhat.com>
- Add lilv to BuildRequires

* Sun Nov 14 2021 Peter Hutterer <peter.hutterer@redhat.com>
- Sync the v4l2 bits from Fedora's pipewire.spec

* Sun Nov 14 2021 Peter Hutterer <peter.hutterer@redhat.com>
- BuildRequire openssl-devel

* Tue Oct 19 2021 Peter Hutterer <peter.hutterer@redhat.com>
- drop media-session, it's its own package now

* Mon Oct 18 2021 Peter Hutterer <peter.hutterer@redhat.com>
- copr autobuild from git setup
