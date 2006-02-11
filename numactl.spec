Summary:	Simple NUMA policy support
Summary(pl):	Prosta obs³uga polityk NUMA
Name:		numactl
Version:	0.9.2
Release:	1
License:	LGPL v2.1 (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://ftp.suse.com/pub/people/ak/numa/%{name}-%{version}.tar.gz
# Source0-md5:	8bac0d50c70f6de63cbf15546cca6044
URL:		ftp://ftp.suse.com/pub/people/ak/numa/
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Simple NUMA policy support. It consists of a numactl program to run
other programs with a specific NUMA policy and a libnuma to do
allocations with NUMA policy in applications.

%description -l pl
Prosta obs³uga polityk NUMA. Pakiet zawiera program numactl do
uruchamiania innych programów z okre¶lon± polityk± NUMA oraz libnuma
do przydzielania pamiêci z polityk± NUMA w aplikacjach.

%package devel
Summary:	Header files for libnuma library
Summary(pl):	Pliki nag³ówkowe biblioteki libnuma
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libnuma library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libnuma.

%prep
%setup -q

rm -f *.o

%build
%{__make} \
	CC="%{__cc}" \
	OPT_CFLAGS="%{rpmcflags} -Wall"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir}/man{2,3,8}}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

# missing in make install
install get_mempolicy.2 $RPM_BUILD_ROOT%{_mandir}/man2

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
%{_mandir}/man8/numactl.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnuma.so
%{_includedir}/numa*.h
%{_mandir}/man2/get_mempolicy.2*
%{_mandir}/man2/set_mempolicy.2*
%{_mandir}/man2/mbind.2*
%{_mandir}/man3/*
