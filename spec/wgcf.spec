%define debug_package %{nil}

Name:           wgcf
Version:        2.2.8
Release:        1%{?dist}
Summary:        Cross-platform, unofficial CLI for Cloudflare Warp.
License:        MIT
URL:            https://github.com/ViRb3/wgcf/
Source0:        %{url}/archive/v%version.tar.gz
BuildRequires:  git golang

%description
%{summary}

%prep
%autosetup -n %{name}-%{version}

%build
go build -v

%install
install -p -D -m755 %{name}         %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
