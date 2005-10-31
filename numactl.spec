Summary:	Simple NUMA policy support
Summary(pl):	Prosta obs�uga polityk NUMA
Name:		numactl
Version:	0.6.4
Release:	1
License:	LGPL v2.1 (library), GPL v2 (utilities)
Group:		Applications/System
Source0:	ftp://ftp.suse.com/pub/people/ak/numa/%{name}-%{version}.tar.gz
# Source0-md5:	4d79d74c69637e1d2a5d64dfc2662fab
URL:		ftp://ftp.suse.com/pub/people/ak/numa/
BuildRequires:	sed >= 4.0
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

sed -i -e 's/-g /%{rpmcflags} /' Makefile

%build
%{__make} \
	CC="%{__cc}"

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
%attr(755,root,root) %{_bindir}/numactl
%attr(755,root,root) %{_bindir}/numademo
%attr(755,root,root) %{_bindir}/numastat
%attr(755,root,root) %{_bindir}/memhog
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
