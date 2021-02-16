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
%autosetup -n BLAKE3-%version

%build
cargo build --release --manifest-path b3sum/Cargo.toml

%install
install -p -D -m755 b3sum/target/release/%{name}         %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}
