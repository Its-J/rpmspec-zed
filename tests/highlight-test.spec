%global commit      ec86047d67acd6fddd81392f44ed6ebcc6e7f531
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commit_date 20261027
%define major       1
%define minor       27
%define patchlevel  0
%define pyver       3.13

%define with_opts(n:v) echo %1 %2 %* %#
%global negated %!name
%global computed %{expr: 1.5 + 2}
%global lua_version %{lua: print(rpm.expand("%{major}") .. "." .. rpm.expand("%{minor}")) }
%global build_host %(hostname -s 2>/dev/null || echo unknown)
%global printf_fmt %%s-%%d

%undefine _auto_set_build_flags

%bcond_with    check
%bcond_without docs
%bcond         nightly 0
%bcond         lto 1

%if 0%{?fedora} >= 40 && 0%{?rhel} == 0
%global distro_ok 1
%elif 0%{?rhel} > 9 || 0%{?centos} != 0
%global distro_ok 2
%else
%global distro_ok 0
%endif

%if %{defined fedora} && %{undefined rhel}
%global is_fedora 1
%endif

%if %{with nightly} and %{without lto}
%global nightly_nolto 1
%endif

%if "%{_vendor}" == "redhat" or "%{_vendor}" != "suse"
%global vendor_ok 1
%endif

%if %{major} < 2 && %{minor} <= 30
%global old_series 1
%endif

%ifarch x86_64 aarch64
%global has_simd 1
%elifarch ppc64le s390x
%global has_simd 0
%endif

%ifnarch %{ix86} %{arm}
%global native_64 1
%endif

%ifos linux
%global is_linux 1
%elifos freebsd
%global is_linux 0
%endif

%ifnos windows
%global not_windows 1
%endif

%if !%{with check}
%global skip_tests 1
%endif

# comment
%dnl line comment with a macro %{name} in it
%global dnl_colon a%{dnl:inline comment %{_bindir}}b
%global dnl_space a%{dnl inline comment %{_bindir}}b
%global dnl_empty a%{dnl}b
%if %{?debug_package:1}%{!?debug_package:0}
%global debug_package %{nil}
%endif

Name:           highlight-test
Version:        %{major}.%{minor}.%{patchlevel}
Release:        1.%{commit_date}git%{shortcommit}%{?dist}
Epoch:          2
Summary:        Highlighting test spec
License:        %{SourceLicense} AND MIT AND (Apache-2.0 OR BSD-3-Clause)
URL:            https://github.com/Its-J/rpmspec-zed
VCS:            git:https://github.com/Its-J/rpmspec-zed.git
Group:          Development/Tools
Vendor:         Fyra Labs
Packager:       Its-J <jonah@fyralabs.com>
Distribution:   Terra
BugURL:         https://github.com/Its-J/rpmspec-zed/issues
BuildArch:      noarch
ExclusiveArch:  x86_64 aarch64
ExcludeArch:    %{ix86} ppc64le
ExclusiveOS:    linux
AutoReqProv:    yes
AutoReq:        no
AutoProv:       yes
Summary(de):    Testspezifikation für Hervorhebung
Group(de):      Entwicklung/Werkzeuge
SourceLicense:  MIT
DistTag:        terra
ModularityLabel: highlight:1:0:x86_64
Url:            https://github.com/Its-J/rpmspec-zed
BugUrl:         https://github.com/Its-J/rpmspec-zed/issues
BuildArchitectures: noarch
ExcludeOS:      windows
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildSystem:    cmake
BuildOption:    -DFOO=ON
BuildOption(conf): -DBAR=OFF
BuildOption(build): -j4
BuildOption(install): prefix=%{_prefix}
DocDir:         %{_docdir}
Prefix:         /usr
Prefixes:       /usr /etc
RemovePathPostfixes: .compat

Source0:        https://github.com/Its-J/rpmspec-zed/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        %{name}.desktop
Source2:        %{name}.metainfo.xml
Source10:       ftp://ftp.example.org/pub/extra-%{version}.tar.xz
Source:         README.fedora
NoSource:       10

Patch0:         0001-fix-build.patch
Patch1:         0002-%{name}-use-system-libs.patch
Patch100:       https://example.org/patches/upstream-%{version}.patch
Patch:          unnumbered.patch
NoPatch:        100

BuildRequires:  gcc, gcc-c++, git-core
buildrequires:  make
BuildRequires:  cmake >= 3.20
BuildRequires:  meson > 1.0
BuildRequires:  ninja-build = 1.11.1
BuildRequires:  python3-devel <= %{pyver}
BuildRequires:  rust < 2.0
BuildRequires:  cargo-rpm-macros >= 24 pkgconfig(openssl) >= 3.0.0

BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  perl(File::Temp)
BuildRequires:  python3dist(setuptools) >= 61
BuildRequires:  crate(serde/default) >= 1.0
BuildRequires:  golang(github.com/spf13/cobra)

Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:       glibc(x86-64)
Requires:       zlib(x86-32)
Requires:       libffi(aarch64)
Requires:       openssl-libs(ppc-64)
Requires:       libgcc(ppc-32)
Requires:       libstdc++(s390x)
Requires:       pcre2(arm)

Requires:       /usr/bin/pkg-config
BuildRequires:  /usr/bin/desktop-file-validate

Requires:       libc.so.6(GLIBC_2.34)(64bit)
Requires:       libz.so.1()(64bit)

Requires:       (foo or bar)
Requires:       (pkgA if pkgB else pkgC)
Requires:       (pkgA unless pkgB)
Requires:       (gtk4 with gtk4-devel)
Requires:       (python3 without python3-libs)
Requires:       ((foo >= 1.0 and bar < 2.0) or baz)

Requires(pre):         shadow-utils
Requires(post):        systemd
Requires(preun):       systemd
Requires(postun):      systemd
Requires(pretrans):    coreutils
Requires(posttrans):   coreutils
Requires(post,postun): /sbin/ldconfig
Requires(interp):      /usr/bin/lua
Requires(meta):        %{name}-data
Requires(verify):      coreutils
BuildPrereq:    autoconf
Prereq:         coreutils
OrderWithRequires(post): firewalld
OrderWithRequires: firewalld

Provides:       %{name}-compat = %{version}-%{release}
Provides:       bundled(crate(serde)) = 1.0.200
  Provides:     indented-since-4-20
Obsoletes:      old-highlight-test < 1.0
Conflicts:      highlight-test-legacy
Recommends:     bash-completion
Recommends(meta): bash-completion-extras
Suggests:       zed
Enhances:       zed
Supplements:    (%{name} and langpacks-en)
BuildConflicts: clang < 15

%description
Macros expand in here too: %{name}, %{version}, %{?dist}, %{!?dist:no-dist}.

%if %{with docs}
Only present when built --with docs.
%endif

%package        libs
Summary:        Shared libraries for %{name}
Requires:       glibc%{?_isa}

%description    libs
Runtime libraries for %{name}.

%package -n     python3-%{name}
Summary:        Python bindings for %{name}
Requires:       %{name}-libs = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 bindings for %{name}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Headers and pkg-config files for %{name}.

%package        doc
Summary:        Documentation for %{name}

%description    doc
HTML documentation for %{name}.

%sourcelist
https://example.org/extra/data-%{version}.tar.gz
local-config.toml
%{name}-sysusers.conf

%patchlist
0100-sourcelist-patch.patch
https://example.org/patches/0101-remote.patch

%prep
%setup -q -n %{name}-%{commit}
%setup -q -T -D -a 1 -b 2 -c -n other-dir
%autosetup -p1 -n %{name}-%{commit}
%autosetup -S git -N -v
%patch 0 -p1
%patch 1 -p1 -b .system-libs
%patch -P 100 -p1 -R
%autopatch -p1 -m 100 -M 199
%autopatch -v 0 1

cp -p %{SOURCE1} %{SOURCE2} .
sed -i 's|/usr/local|%{_prefix}|g' Makefile
find . -name '*.orig' -delete

%if %{with lto}
echo "LTO enabled"
%else
echo "LTO disabled"
%endif

%generate_buildrequires
%pyproject_buildrequires -x test

%conf
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DENABLE_TESTS=%{?with_check:ON}%{!?with_check:OFF}
./configure --prefix=%{_prefix} --libdir=%{_libdir} --disable-static

%build
export CFLAGS="%{optflags} -fno-strict-aliasing"
%make_build
%cargo_build -f feature-a,feature-b
%{__python3} setup.py build
make %{?_smp_mflags} V=1 CC="%{__cc}"
%dnl make %{?_smp_mflags} check
make %{dnl:-j1} install-docs

for f in docs/*.md; do
    pandoc -s "$f" -o "${f%%.md}.html"
done

if [ -n "$SOURCE_DATE_EPOCH" ]; then
    touch -d "@${SOURCE_DATE_EPOCH}" build.stamp
fi

%build -a
echo "appended build step" >> build.log

%install
%make_install DESTDIR=%{buildroot}
%pyproject_install
%pyproject_save_files -l highlight_test
install -Dpm 0755 build/%{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
ln -sf %{_bindir}/%{name} %{buildroot}%{_bindir}/ht
%find_lang %{name}
%{!?_licensedir:%global license %%doc}

%install -p
echo "runs before the main install"

%check
%if %{with check}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%pytest -v -k "not slow"
%endif

%clean
rm -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
exit 0

%post
%systemd_post %{name}.service
if [ $1 -eq 1 ]; then
    echo "first install"
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%pretrans
echo "pretrans"

%posttrans
echo "posttrans"

%preuntrans
echo "preuntrans"

%postuntrans
echo "postuntrans"

%verify
test -x %{_bindir}/%{name}

%post libs -p /sbin/ldconfig

%pretrans -p <lua>
local path = "/usr/share/%{name}"
local st = posix.stat(path)
if st and st.type == "link" then
    os.remove(path)
end

%post -n python3-%{name} -p /usr/bin/python3
import sys
print("installed for python", sys.version_info[:2])

%postun devel -p /usr/bin/perl
use strict;
my @files = glob("/usr/include/%{name}/*.h");
print scalar(@files), " headers left\n";

%preun doc -p /bin/bash
[[ $1 -eq 0 ]] && echo "removing docs"

%posttrans doc -p /bin/sh
echo "doc posttrans"

%triggerprein -- zed < 1.0
echo "zed is about to be installed"

%triggerin -- zed
echo "zed installed or upgraded"

%triggerun -- zed
echo "zed being removed"

%triggerpostun -- zed < 0.150
echo "zed old version removed"

%triggerin -p <lua> -- glibc
print("glibc changed: " .. tostring(arg[2]))

%triggerun -p /usr/bin/perl -- perl
print "perl being removed\n";

%filetriggerin -- %{_datadir}/applications
update-desktop-database -q || :

%filetriggerun -- %{_libdir}
/sbin/ldconfig

%filetriggerpostun -P 1000 -- %{_datadir}/icons
gtk-update-icon-cache -q %{_datadir}/icons/hicolor || :

%transfiletriggerin -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%transfiletriggerun -p <lua> -- %{_libdir}
print("libs going away")

%transfiletriggerpostun -- %{_datadir}/glib-2.0/schemas
glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :

%files -f %{name}.lang -f %{pyproject_files}
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/%{name}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%attr(0750, %{name}, %{name}) %dir %{_localstatedir}/lib/%{name}
%verify(not md5 size mtime) %{_localstatedir}/lib/%{name}/state
%ghost %attr(0600, root, root) %{_rundir}/%{name}.pid
%caps(cap_net_bind_service=ep) %{_bindir}/%{name}-server
%exclude %{_bindir}/%{name}-debug
%missingok %{_sysconfdir}/%{name}/optional.conf
%readme NOTES.txt
%docdir %{_datadir}/%{name}/manual
%artifact %{_prefix}/lib/.build-id/xx/yyyy
%{_mandir}/man1/%{name}.1*

%ifarch x86_64
%{_libexecdir}/%{name}/simd-helper
%endif

%files libs
%defattr(-, root, root, 0755)
%{_libdir}/lib%{name}.so.%{major}{,.*}

%files -n python3-%{name} -f %{pyproject_files}
%doc README.md

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%doc docs/*.htmlrpmba

%changelog
* Thu Oct 29 2026 Its-J <jonah@fyralabs.com> - 2:1.27.0-1
- %%{excaped_macro}
