%global kf5_version 5.99.0

# uncomment to enable bootstrap mode
#global bootstrap 1

%if !0%{?bootstrap}
%global tests 1
%endif

Name:    kf5-kirigami2
Version: 5.99.0
Release: 1%{?dist}
Summary: QtQuick plugins to build user interfaces based on the KDE UX guidelines

# All LGPLv2+ except for src/desktopicons.h (GPLv2+)
License: GPLv2+
URL:     https://techbase.kde.org/Kirigami

%global majmin %majmin_ver_kf5
%global stable %stable_kf5
Source0: %{name}-%{version}.tar.bz2

## upstream paches

# filter qml provides
%global __provides_exclude_from ^%{_kf5_qmldir}/.*\\.so$

BuildRequires: make
BuildRequires: extra-cmake-modules >= %{kf5_version}
#BuildRequires: kf5-rpm-macros

BuildRequires: opt-qt5-linguist
BuildRequires: opt-qt5-qtbase-devel
BuildRequires: opt-qt5-qtdeclarative-devel
BuildRequires: opt-qt5-qtquickcontrols2-devel
BuildRequires: opt-qt5-qtsvg-devel
BuildRequires: opt-qt5-qtbase-private-devel
Requires:      opt-qt5-qtquickcontrols%{?_isa}
Requires:      opt-qt5-qtquickcontrols2%{?_isa}

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
# strictly not required, but some consumers may assume/expect runtime bits to be present too
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

mkdir -p build
pushd build

%{_opt_cmake_kf5} ../ \
  -DBUILD_TESTING:BOOL=%{?tests:ON}%{!?tests:OFF}
make
popd

%install
pushd build
make DESTDIR=%{buildroot} install
popd
%find_lang_kf5 libkirigami2plugin_qt


%check
%if 0%{?tests}
## known failure(s), not sure if possible to enable opengl/glx using
## virtualized server (QT_XCB_FORCE_SOFTWARE_OPENGL doesn't seem to help)
#2/2 Test #2: qmltests .........................***Exception: Other  0.19 sec
#Could not initialize GLX
export QT_XCB_FORCE_SOFTWARE_OPENGL=1
export CTEST_OUTPUT_ON_FAILURE=1
xvfb-run -a \
make test ARGS="--output-on-failure --timeout 30" -C %{_target_platform} ||:
%endif


%files
%license LICENSES/*.txt
%{_opt_kf5_libdir}/libKF5Kirigami2.so.5*
%dir %{_opt_kf5_qmldir}/org/
%dir %{_opt_kf5_qmldir}/org/kde/
%{_opt_kf5_qmldir}/org/kde/kirigami.2/
%{_opt_kf5_datadir}/locale/

%files devel
%{_opt_kf5_libdir}/libKF5Kirigami2.so
%{_opt_kf5_includedir}/KF5/Kirigami2/
%{_opt_kf5_archdatadir}/mkspecs/modules/qt_Kirigami2.pri
%{_opt_kf5_libdir}/cmake/KF5Kirigami2/
%dir %{_opt_kf5_datadir}/kdevappwizard/
%dir %{_opt_kf5_datadir}/kdevappwizard/templates/
%{_opt_kf5_datadir}/kdevappwizard/templates/kirigami.tar.bz2