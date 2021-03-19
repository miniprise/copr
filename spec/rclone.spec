%define debug_package %{nil}

Name:           rclone
Version:        1.54.1
Release:        1{?dist}
Summary:        rclone from copr
License:        MIT
URL:            https://github.com/rclone/rclone
Source0:        https://github.com/rclone/%{name}/archive/v%{version}.tar.gz
BuildRequires:  git golang

%description
"rsync for cloud storage" - Google Drive, S3, Dropbox, Backblaze B2, One Drive, Swift, Hubic, Wasabi, Google Cloud Storage, Yandex Files...

%prep
%autosetup -n %{name}-%{version}

%build
go build -v

%install
install -p -D -m755 %{name}         %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 ./rclone.1 %{buildroot}%{_mandir}/man1/rclone.1

%files
%{_bindir}/%{name}
%{_mandir}/man1/rclone.1*

%changelog
* Sat Feb 13 2021 Miniprise <miniprise@protonmail.com> - 1.54.0
- Update rclone to latest version
