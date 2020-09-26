#
# Conditional build:
%bcond_without	static_libs	# static libraries

Summary:	Utility library for software from Belledonne Communications
Summary(pl.UTF-8):	Biblioteka narzędziowa dla oprogramowania firmy Belledonne Communications
Name:		bctoolbox
Version:	4.4.0
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/bctoolbox/tags
Source0:	https://gitlab.linphone.org/BC/public/bctoolbox/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	b1239d1aebca6acdf5662d5970c159ab
URL:		https://linphone.org/
# with junit xml support
BuildRequires:	bcunit-devel >= 3.0.2-3.20200822
BuildRequires:	cmake >= 2.8.12
BuildRequires:	libdecaf-devel
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	mbedtls-devel
BuildRequires:	sed >= 4.0
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
Requires:	libdecaf-devel
Requires:	mbedtls-devel

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

%build
install -d build
cd build
%cmake .. \
	%{!?with_static_libs:-DENABLE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_datadir}/bctoolbox/cmake/bctoolboxTargets.cmake

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
%attr(755,root,root) %{_libdir}/libbctoolbox.so
%attr(755,root,root) %{_libdir}/libbctoolbox-tester.so
%{_includedir}/bctoolbox
%{_pkgconfigdir}/bctoolbox.pc
%{_pkgconfigdir}/bctoolbox-tester.pc
%dir %{_datadir}/bctoolbox
%{_datadir}/bctoolbox/cmake

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbctoolbox.a
%{_libdir}/libbctoolbox-tester.a
%endif
