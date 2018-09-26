Summary:	Utility library for software from Belledonne Communications
Name:		bctoolbox
Version:	0.6.0
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/bctoolbox/%{name}-%{version}.tar.gz
# Source0-md5:	aeeac76938dd3b82a17ff498f81caef2
URL:		https://linphone.org/
BuildRequires:	bcunit-devel
BuildRequires:	cmake
BuildRequires:	mbedtls-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities library used by Belledonne Communications softwares like
belle-sip, mediastreamer2 and linphone.

%package devel
Summary:	Header files and develpment documentation for bctoolbox
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and develpment documentation for bctoolbox.

%prep
%setup -q

%build
install -d build
cd build
%{cmake} ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libbctoolbox.so.*
%attr(755,root,root) %{_libdir}/libbctoolbox-tester.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbctoolbox.so
%attr(755,root,root) %{_libdir}/libbctoolbox-tester.so
%{_includedir}/bctoolbox
%{_pkgconfigdir}/bctoolbox.pc
%{_pkgconfigdir}/bctoolbox-tester.pc
%{_datadir}/bctoolbox
