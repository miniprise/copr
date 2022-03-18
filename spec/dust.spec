%define debug_package %{nil}

Name:          dust
Version:       0.8.1-alpha.2
Release:       1%{?dist}
Summary:       A more intuitive version of du in rust 
License:       Apache

URL:           https://github.com/bootandy/dust
Source0:       https://transfer.sh/get/bQEaFo/dust-0.8.1.tar.xz

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
