%define debug_package %{nil}

Name:          bat
Version:       0.18.0
Release:       1%{?dist}
Summary:       A cat(1) clone with wings.
License:       Apache-2.0

URL:           https://github.com/sharkdp/bat/
Source0:       %{url}/archive/v%version.tar.gz

BuildRequires: rust
BuildRequires: cargo

%description
%{summary}.

%prep
%autosetup

%build
cargo build --release

%install
install -p -D -m755 target/release/%{name}         %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
