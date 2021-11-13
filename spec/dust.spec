%define debug_package %{nil}

Name:          dust
Version:       0.7.5
Release:       1%{?dist}
Summary:       A more intuitive version of du in rust 
License:       Apache

URL:           https://github.com/bootandy/dust
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
