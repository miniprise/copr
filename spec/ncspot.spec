%define debug_package %{nil}

Name:          ncspot
Version:       0.9.5
Release:       1%{?dist}
Summary:       ncurses Spotify client written in Rust using librespot
License:       BSD

URL:           https://github.com/hrkfdn/ncspot
Source0:       %{url}/archive/v%version.tar.gz

BuildRequires: rust
BuildRequires: cargo
BuildRequires: pulseaudio-libs-devel
BuildRequires: libxcb-devel
BuildRequires: openssl-devel
BuildRequires: ncurses-devel
BuildRequires: dbus-devel

%description
%{summary}.

%prep
%autosetup

%build
cargo build --release

%install
install -p -D -m755 target/release/%{name}         %{buildroot}%{_bindir}/%{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
