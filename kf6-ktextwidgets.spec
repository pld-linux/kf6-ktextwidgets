#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.19
%define		qtver		5.15.2
%define		kfname		ktextwidgets

Summary:	Text editing widgets
Name:		kf6-%{kfname}
Version:	6.19.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	221b9c05e0da3426c8f91893e5c03581
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6TextToSpeech-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	kf6-kcompletion-devel >= %{version}
BuildRequires:	kf6-kconfig-devel >= %{version}
BuildRequires:	kf6-kconfigwidgets-devel >= %{version}
BuildRequires:	kf6-ki18n-devel >= %{version}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{version}
BuildRequires:	kf6-sonnet-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6TextToSpeech >= %{qtver}
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
Requires:	kf6-kcompletion >= %{version}
Requires:	kf6-kconfig >= %{version}
Requires:	kf6-kconfigwidgets >= %{version}
Requires:	kf6-ki18n >= %{version}
Requires:	kf6-kwidgetsaddons >= %{version}
Requires:	kf6-sonnet >= %{version}
#Obsoletes:	kf5-%{kfname} < %{version}
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KTextWidgets provides widgets for displaying and editing text. It
supports rich text as well as plain text.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	kf6-ki18n-devel >= %{version}
Requires:	kf6-sonnet-devel >= %{version}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}6

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}6.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6TextWidgets.so.6
%{_libdir}/libKF6TextWidgets.so.*.*
%{_libdir}/qt6/plugins/designer/ktextwidgets6widgets.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KTextWidgets
%{_libdir}/cmake/KF6TextWidgets
%{_libdir}/libKF6TextWidgets.so
