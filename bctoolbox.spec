#
# Conditional build:
%bcond_without	dtls_srtp	# DTLS SRTP support
%bcond_without	static_libs	# static libraries

%define		mbedtls_ver	3
Summary:	Utility library for software from Belledonne Communications
Summary(pl.UTF-8):	Biblioteka narzędziowa dla oprogramowania firmy Belledonne Communications
Name:		bctoolbox
Version:	5.4.17
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bctoolbox/tags
Source0:	https://gitlab.linphone.org/BC/public/bctoolbox/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	c5bf3fdbbe08df0c1e28f0a927d96fff
Patch0:		%{name}-decaf-shared.patch
Patch1:		%{name}-mbedtls.patch
URL:		https://linphone.org/
BuildRequires:	bcunit-devel >= 5.3.0
BuildRequires:	cmake >= 3.22
BuildRequires:	libdecaf-devel >= 1.0.2
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	mbedtls-devel >= %{mbedtls_ver}
BuildRequires:	sed >= 4.0
Requires:	libdecaf >= 1.0.2
Requires:	mbedtls >= %{mbedtls_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utilities library used by Belledonne Communications softwares like
belle-sip, mediastreamer2 and linphone.

%description -l pl.UTF-8
Biblioteka narzędziowa używana w oprogramowaniu firmy Belledonne
Communications, takim jak belle-sip, mediastreamer2 czy linphone.

%package devel
Summary:	Header files for bctoolbox libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek bctoolbox
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libdecaf-devel >= 1.0.2
Requires:	mbedtls-devel >= %{mbedtls_ver}

%description devel
Header files for bctoolbox libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek bctoolbox.

%package static
Summary:	Static bctoolbox libraries
Summary(pl.UTF-8):	Statyczne biblioteki bctoolbox
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static bctoolbox libraries.

%description static -l pl.UTF-8
Statyczne biblioteki bctoolbox.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%build
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF \
	-DENABLE_UNIT_TESTS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir

%{__make} -C builddir

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbctoolbox.so.1
%attr(755,root,root) %{_libdir}/libbctoolbox-tester.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bctoolbox-tester
%attr(755,root,root) %{_libdir}/libbctoolbox.so
%attr(755,root,root) %{_libdir}/libbctoolbox-tester.so
%{_includedir}/bctoolbox
%{_pkgconfigdir}/bctoolbox.pc
%{_pkgconfigdir}/bctoolbox-tester.pc
%dir %{_datadir}/BCToolbox
%{_datadir}/BCToolbox/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbctoolbox.a
%{_libdir}/libbctoolbox-tester.a
%endif
