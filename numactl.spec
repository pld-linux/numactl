Summary:	Simple NUMA policy support
Summary(pl.UTF-8):	Prosta obsługa polityk NUMA
Name:		numactl
Version:	2.0.11
Release:	1
License:	LGPL v2.1 (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://oss.sgi.com/www/projects/libnuma/download/%{name}-%{version}.tar.gz
# Source0-md5:	d3bc88b7ddb9f06d60898f4816ae9127
URL:		http://oss.sgi.com/projects/libnuma/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy and a libnuma to do
allocations with NUMA policy in applications.

%description -l pl.UTF-8
Prosta obsługa polityk NUMA. Pakiet zawiera program numactl do
uruchamiania innych programów z określoną polityką NUMA oraz libnuma
do przydzielania pamięci z polityką NUMA w aplikacjach.

%package devel
Summary:	Header files for libnuma library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnuma
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libnuma library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnuma.

%package static
Summary:	Static libnuma library
Summary(pl.UTF-8):	Statyczna biblioteka libnuma
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnuma library.

%description static -l pl.UTF-8
Statyczna biblioteka libnuma.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not needed (library without external dependencies)
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnuma.la
# in man-pages (it's Linux syscall, although API is defined in numaif.h)
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man2/move_pages.2

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
# it used to be library itself, now it's SONAME symlink
if [ -f %{_libdir}/libnuma.so.1 ]; then
	rm -f %{_libdir}/libnuma.so.1
fi

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%attr(755,root,root) %{_bindir}/memhog
%attr(755,root,root) %{_bindir}/migratepages
%attr(755,root,root) %{_bindir}/migspeed
%attr(755,root,root) %{_bindir}/numactl
%attr(755,root,root) %{_bindir}/numademo
%attr(755,root,root) %{_bindir}/numastat
%attr(755,root,root) %{_libdir}/libnuma.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnuma.so.1
%{_mandir}/man8/migratepages.8*
%{_mandir}/man8/migspeed.8*
%{_mandir}/man8/numactl.8*
%{_mandir}/man8/numastat.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuma.so
%{_includedir}/numa*.h
%{_mandir}/man3/numa.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libnuma.a
