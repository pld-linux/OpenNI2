#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	java		# Java wrappers
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions
%bcond_with	ssse3		# use SSE3 and SSSE3 instructions

%if %{with ssse3}
%define	with_sse3	1
%endif
Summary:	OpenNI2 framework for Natural Interaction devices
Summary(pl.UTF-8):	Szkielet OpenNI2 do urządzeń służących interakcji z naturą
Name:		OpenNI2
Version:	2.2.0.33
%define	subver	beta2
%define	rel	4
Release:	0.%{subver}.%{rel}
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/structureio/OpenNI2/tags
Source0:	https://github.com/structureio/OpenNI2/archive/2.2-%{subver}/%{name}-%{version}.tar.gz
# Source0-md5:	3f2cd6a64776821fb2837c442539f65b
Patch0:		%{name}-system-libs.patch
Patch1:		%{name}-nosse.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-paths.patch
Patch4:		%{name}-soname.patch
Patch5:		%{name}-norpath.patch
Patch6:		%{name}-defines.patch
Patch7:		%{name}-nowarn.patch
Patch8:		%{name}-c++.patch
URL:		http://structure.io/openni
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-glut-devel >= 3
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
%{?with_java:BuildRequires:	jdk >= 1.6.0}
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel >= 6:4.0
BuildRequires:	libusb-devel >= 1.0.8
BuildRequires:	python >= 1:2.6
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.566
BuildRequires:	sed >= 4.0
BuildRequires:	udev-devel
# NOTE: other platforms need adding a dozen of defines in Include/Linux-*/*.h
ExclusiveArch:	%{ix86} %{x8664} x32 %{arm}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86}
%define		openni_platform	x86
%endif
%ifarch %{x8664} x32
%define		openni_platform	x64
%endif
%ifarch %{arm}
%define		openni_platform	Arm
%endif

%description
OpenNI2 framework provides an application programming interface (API)
for writing applications utilizing natural interaction. This API
covers communication with both low level devices (e.g. vision and
audio sensors), as well as high-level middleware solutions (e.g. for
visual tracking using computer vision).

The OpenNI2 Framework provides the interface for physical devices and
for middleware components. The API enables modules to be registered in
the OpenNI2 framework and used to produce sensory data. Selecting the
hardware or middleware module is easy and flexible.

%description -l pl.UTF-8
Szkielet OpenNI2 zapewnia interfejs programistyczny (API) dla
aplikacji wykorzystujących interakcję z naturą. API to pokrywa
komunikację zarówno z urządzeniami niskiego poziomu (takimi jak
czujniki obrazu i dźwięku), jak i rozwiązaniami wysokiego poziomu
warstwy pośredniej (np. do wizualnego śledzenia przy użyciu obrazu
komputerowego).

Szkielet OpenNI2 zapewnia interfejs dla fizycznych urządzeń oraz
komponentów warstwy pośredniej. API pozwala na rejestrowanie modułów w
szkielecie OpenNI2 i wykorzystywanie do tworzenia danych
sensorycznych. Wybór sprzętu i modułu pośredniego jest prosty i
elastyczny.

%package devel
Summary:	Header files for OpenNI2 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenNI2
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenNI2 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenNI2.

%package apidocs
Summary:	OpenNI2 API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki OpenNI2
Group:		Documentation
BuildArch:	noarch

%description apidocs
API and internal documentation for OpenNI2 library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki OpenNI2.

%package -n java-OpenNI2
Summary:	Java wrapper for OpenNI2
Summary(pl.UTF-8):	Interfejs Javy do OpenNI2
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}
Requires:	jpackage-utils
Requires:	jre >= 1.6.0

%description -n java-OpenNI2
Java wrapper for OpenNI2.

%description -n java-OpenNI2 -l pl.UTF-8
Interfejs Javy do OpenNI2.

%prep
%setup -q -n %{name}-2.2-%{subver}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

%build
export CFLAGS="%{rpmcflags} -Wno-unused-local-typedefs -Wno-enum-compare -Wno-unused-local-typedefs -Wno-misleading-indentation"
export CXXFLAGS="%{rpmcxxflags} -Wno-unused-local-typedefs -Wno-enum-compare -Wno-unused-local-typedefs -Wno-misleading-indentation"
%{__make} \
	CFG=Release \
	CXX="%{__cxx}" \
	HOSTPLATFORM=%{openni_platform} \
	SSE_GENERATION=%{?with_sse3:3}%{!?with_sse3:%{?with_sse2:2}} \
	%{?with_ssse3:SSSE3_ENABLED=1} \
	%{!?with_java:ALL_JAVA_PROJS= JAVA_SAMPLES=}

%if %{with apidocs}
cd Source/Documentation
doxygen Doxyfile
%if %{with java}
# fails with "unknown tag" errors since Java 8
#javadoc -d java $(find ../../Wrappers/java/OpenNI.java/src/org/openni -type f)
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/OpenNI2/Drivers,%{_pkgconfigdir},%{_includedir}/openni2,/lib/udev/rules.d}

# upstream "install" - no FHS support
#Packaging/Harvest.py $RPM_BUILD_ROOT %{openni_platform}

BDIR=Bin/%{openni_platform}-Release
install -p ${BDIR}/{NiViewer,PS1080Console,PSLinkConsole} $RPM_BUILD_ROOT%{_bindir}
cp -dpr ${BDIR}/libOpenNI2.so* $RPM_BUILD_ROOT%{_libdir}
cp -p Config/OpenNI.ini $RPM_BUILD_ROOT%{_libdir}
install -p ${BDIR}/OpenNI2/Drivers/*.so $RPM_BUILD_ROOT%{_libdir}/OpenNI2/Drivers
cp -p Config/OpenNI2/Drivers/*.ini $RPM_BUILD_ROOT%{_libdir}/OpenNI2/Drivers
cp -p Packaging/Linux/primesense-usb.rules $RPM_BUILD_ROOT/lib/udev/rules.d/55-primesense-usb.rules
cp -p Include/*.h $RPM_BUILD_ROOT%{_includedir}/openni2
cp -pr Include/Driver $RPM_BUILD_ROOT%{_includedir}/openni2
%ifarch %{ix86} %{x8664} x32
cp -pr Include/Linux-x86 $RPM_BUILD_ROOT%{_includedir}/openni2
%endif
%ifarch %{arm}
cp -pr Include/Linux-Arm $RPM_BUILD_ROOT%{_includedir}/openni2
%endif

cat >$RPM_BUILD_ROOT%{_pkgconfigdir}/libopenni2.pc <<'EOF'
prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}/openni2

Name: OpenNI2
Description: A general purpose driver for all OpenNI cameras.
Version: %{version}-%{subver}
Cflags: -I${includedir}
Libs: -L${libdir} -lOpenNI2
EOF

%if %{with java}
install -d $RPM_BUILD_ROOT%{_javadir}
install -p ${BDIR}/libOpenNI2.jni.so $RPM_BUILD_ROOT%{_libdir}
cp -p ${BDIR}/org.openni.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	-n java-OpenNI2 -p /sbin/ldconfig
%postun	-n java-OpenNI2 -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt NOTICE README ReleaseNotes.txt
%attr(755,root,root) %{_bindir}/NiViewer
%attr(755,root,root) %{_bindir}/PS1080Console
%attr(755,root,root) %{_bindir}/PSLinkConsole
%attr(755,root,root) %{_libdir}/libOpenNI2.so.*.*
%{_libdir}/OpenNI.ini
%dir %{_libdir}/OpenNI2
%dir %{_libdir}/OpenNI2/Drivers
%attr(755,root,root) %{_libdir}/OpenNI2/Drivers/libDummyDevice.so
%attr(755,root,root) %{_libdir}/OpenNI2/Drivers/libOniFile.so
%attr(755,root,root) %{_libdir}/OpenNI2/Drivers/libPS1080.so
%attr(755,root,root) %{_libdir}/OpenNI2/Drivers/libPSLink.so
%{_libdir}/OpenNI2/Drivers/PS1080.ini
%{_libdir}/OpenNI2/Drivers/PSLink.ini
/lib/udev/rules.d/55-primesense-usb.rules

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenNI2.so
%{_includedir}/openni2
%{_pkgconfigdir}/libopenni2.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc Source/Documentation/html/*.{bmp,css,html,js,png}
%endif

%if %{with java}
%files -n java-OpenNI2
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libOpenNI2.jni.so
%{_javadir}/org.openni.jar
%endif
