Summary:	Simple NUMA policy support
Summary(pl):	Prosta obs�uga polityk NUMA
Name:		numactl
Version:	0.9.10
Release:	1
License:	LGPL v2.1 (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://ftp.suse.com/pub/people/ak/numa/%{name}-%{version}.tar.gz
# Source0-md5:	440f34e476ed5528a250edc041da5a41
URL:		ftp://ftp.suse.com/pub/people/ak/numa/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy and a libnuma to do
allocations with NUMA policy in applications.

%description -l pl
Prosta obs�uga polityk NUMA. Pakiet zawiera program numactl do
uruchamiania innych program�w z okre�lon� polityk� NUMA oraz libnuma
do przydzielania pami�ci z polityk� NUMA w aplikacjach.

%package devel
Summary:	Header files for libnuma library
Summary(pl):	Pliki nag��wkowe biblioteki libnuma
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libnuma library.

%description devel -l pl
Pliki nag��wkowe biblioteki libnuma.

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

# missing in make install
install migratepages.8 numastat.8 $RPM_BUILD_ROOT%{_mandir}/man8

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
%attr(755,root,root) %{_bindir}/numactl
%attr(755,root,root) %{_bindir}/numademo
%attr(755,root,root) %{_bindir}/numastat
%attr(755,root,root) %{_libdir}/libnuma.so.*
%{_mandir}/man5/numa_maps.5*
%{_mandir}/man8/migratepages.8*
%{_mandir}/man8/numactl.8*
%{_mandir}/man8/numastat.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuma.so
%{_includedir}/numa*.h
%{_mandir}/man3/*
