%define debug_package %{nil}

Name:          b3sum
Version:       0.3.7
Release:       1%{?dist}
Summary:       A command line utility for calculating BLAKE3 hashes, similar to Coreutils tools like b2sum or md5sum. 
License:       Apache-2.0

URL:           https://github.com/BLAKE3-team/BLAKE3
Source0:       %{url}/archive/%version.tar.gz

BuildRequires: rust
BuildRequires: cargo

%description
%{summary}.

%prep
tar xf BLAKE3-%version.tar.gz
cd BLAKE3-%version

%build
cd b3sum
cargo build --release

%install
install -p -D -m755 target/release/%{name}         %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
