%define debug_package %{nil}

Name:           bisq
Version:        1.5.6
Release:        1%{?dist}
Summary:        bisq from copr
License:        MIT
URL:            https://github.com/bisq-network/bisq/
Source0:        https://github.com/bisq-network/%{name}/archive/v%{version}.tar.gz
BuildRequires:  git git-lfs java wget
Requires:       java

%description
A decentralized bitcoin exchange network 

%prep
%autosetup -n %{name}-%{version}

%build
wget https://raw.githubusercontent.com/miniprise/copr/main/desktop/bisq.desktop
./gradlew build

%install
install -d "%{buildroot}/opt/bisq"
cp -r "desktop/build/app/bin/" "%{buildroot}/opt/bisq"
cp -r "desktop/build/app/lib/" "%{buildroot}/opt/bisq"
cp -r "bisq-desktop" "%{buildroot}/opt/bisq/"
install -d "%{buildroot}/usr/bin"
ln -s "/opt/bisq/bisq-desktop" "%{buildroot}/usr/bin/bisq-desktop"
install -Dm644 bisq.desktop "%{buildroot}/usr/share/applications/bisq.desktop"
install -Dm644 "desktop/package/linux/icon.png" "%{buildroot}/usr/share/pixmaps/bisq.png"

%files
/opt/bisq
/usr/bin/bisq-desktop
/usr/share/applications/bisq.desktop
/usr/share/pixmaps/bisq.png

%changelog
* Sat Feb 13 2021 Miniprise <miniprise@protonmail.com> - 1.5.5
- Init
