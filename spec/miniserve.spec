%define debug_package %{nil}

Name:          miniserve
Version:       0.10.4
Release:       1%{?dist}
Summary:       For when you really just want to serve some files over HTTP right now! 
License:       MIT

URL:           https://github.com/svenstaro/miniserve
Source0:       %{url}/archive/v%version.tar.gz

BuildRequires: rust
BuildRequires: cargo

%description
%{summary}.

%prep
%autosetup

%build
cargo build --release --manifest-path b3sum/Cargo.toml

%install
install -p -D -m755 b3sum/target/release/%{name}         %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
