Summary:	Simple NUMA policy support
Summary(pl.UTF-8):	Prosta obsługa polityk NUMA
Name:		numactl
Version:	2.0.3
Release:	1
License:	LGPL v2.1 (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://oss.sgi.com/www/projects/libnuma/download/%{name}-%{version}.tar.gz
# Source0-md5:	8e4fb249e5f719c25d7f433964fb9220
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

%prep
%setup -q

rm -f *.o

%build
%{__make} \
	CC="%{__cc}" \
	OPT_CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}/man5

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

install migspeed numamon $RPM_BUILD_ROOT%{_bindir}
install move_pages.2 $RPM_BUILD_ROOT%{_mandir}/man2
# missing in make install
install {migratepages,migspeed,numastat}.8 $RPM_BUILD_ROOT%{_mandir}/man8

for f in `find $RPM_BUILD_ROOT%{_mandir}/man3 -type l` ; do
	rm -f $f
	echo '.so numa.3' > $f
done

%clean
rm -rf $RPM_BUILD_ROOT

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
%attr(755,root,root) %{_bindir}/numamon
%attr(755,root,root) %{_bindir}/numastat
%attr(755,root,root) %{_libdir}/libnuma.so.*
%{_mandir}/man8/migratepages.8*
%{_mandir}/man8/migspeed.8*
%{_mandir}/man8/numactl.8*
%{_mandir}/man8/numastat.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuma.so
%{_includedir}/numa*.h
%{_mandir}/man2/*
%{_mandir}/man3/*
