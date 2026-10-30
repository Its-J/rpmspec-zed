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

%define plain_define value
%define no_getopt(-) echo %*
%define auto_macros(x) %0 %** %1 %{1} %{2}
%define multi_line \
    first line \
    second line
%define lua_params(a:) %{lua: print(opt.a or "") print(arg[1] or "")}
%define literal_macro<l> %mymacro
%define oneshot_macro<o> %(date +%%s)

%global form_simple %major
%global form_braced %{major}
%global form_args %{with_opts -n x -v a b}
%global form_args_sep %{with_opts -n x -- -not-an-option}
%global form_colon_arg %{with_opts:a}
%global form_cond %{?dist}
%global form_cond_value %{?dist:has-dist}
%global form_neg_cond %{!?dist:no-dist}
%global form_cond_short %?dist
%global form_neg_cond_short %!?dist
%global form_shell %(echo aa-bb-cc | tr '-' '.')
%global form_expr %[3 + 4 * (1 + %{major})]
%global form_expr_ternary %[1 < 2 ? "true" : "false"]
%global form_expr_version %[v"3.1.0-1" < v"1.0~alpha-2" ? 1 : 0]
%global form_expr_logic %[!(%{major} == 1) || %{minor} >= 2 && "%{major}" != "x"]
%global form_escaped %%{major}
%global form_nested %{?major:%{expand:%{minor}}}
%global form_adjacent %{major}%{minor}%{?dist}
%global form_lua_macros %{lua: print(macros.major .. "." .. macros.minor)}

%global bi_basename %{basename:/usr/bin/foo}
%global bi_dirname %{dirname:/usr/bin/foo}
%global bi_exists %{exists:/etc/os-release}
%global bi_suffix %{suffix:foo.tar.gz}
%global bi_url2path %{url2path:https://example.org/foo.tar.gz}
%global bi_u2p %{u2p:https://example.org/foo.tar.gz}
%global bi_uncompress %{uncompress:foo.tar.gz}
%global bi_xdg %{xdg:config}
%global bi_expand %{expand:%%{major}}
%global bi_macrobody %{macrobody:major}
%global bi_quote %{quote:a b}
%global bi_shescape %{shescape:it's}
%global bi_shrink %{shrink:  a   b  }
%global bi_span %{span:one two}
%global bi_len %{len:hello}
%global bi_lower %{lower:HELLO}
%global bi_upper %{upper:hello}
%global bi_reverse %{reverse:hello}
%global bi_gsub %{gsub hello-world - _}
%global bi_rep %{rep ab 3 -}
%global bi_sub %{sub hello 2 4}
%global bi_getenv %{getenv:HOME}
%global bi_getncpus %{getncpus}
%global bi_getncpus_kind %{getncpus:proc}
%global bi_getconfdir %{getconfdir}
%global bi_rpmversion %{rpmversion}
%global bi_verbose %{verbose}
%global bi_verbose_str %{verbose:loud}
%global bi_file_name %{__file_name}
%global bi_file_lineno %{__file_lineno}
%global bi_source %{S:1}
%global bi_patch %{P:0}
%{echo:printed to stdout}
%{warn:printed to stderr}
%{load:/dev/null}
%{dump}
%{trace}
%{trace}

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
SourceLicense:  Apache-2.0 AND GPL-3.0-or-later
License:        %{SourceLicense} AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND ((MIT OR Apache-2.0) AND NCSA) AND ((MIT OR Apache-2.0) AND Unicode-3.0) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 AND ISC) AND (Apache-2.0 OR BSL-1.0 OR MIT) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR GPL-2.0-only) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 OR MIT/BSL-1.0/CC0-1.0) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception) AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR MIT OR Apache-2.0) AND BSD-2-Clause AND (CC0-1.0 OR Apache-2.0 OR Apache-2.0 WITH LLVM-exception) AND (CC0-1.0 OR Apache-2.0) AND (CC0-1.0 OR MIT-0 OR Apache-2.0) AND CC0-1.0 AND GPL-3.0-or-later AND (ISC AND (Apache-2.0 OR ISC) AND OpenSSL) AND (ISC AND (Apache-2.0 OR ISC)) AND ISC AND (MIT AND (MIT OR Apache-2.0)) AND (MIT AND BSD-3-Clause) AND (MIT OR Apache-2.0 OR CC0-1.0) AND (MIT OR Apache-2.0 OR NCSA) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND MIT AND MPL-2.0 AND Unicode-3.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT) AND Zlib
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
DistURL:        https://terra.fyralabs.com
Icon:           highlight-test.xpm
TranslationUrl: https://translate.example.org/projects/highlight-test
UpstreamReleases: https://github.com/Its-J/rpmspec-zed/releases
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

BuildRequires(pre): example

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
Requires(preuntrans):  coreutils
Requires(postuntrans): coreutils
Requires(meta):        %{name}-data
Requires(verify):      coreutils
Requires(rpmlib):      rpmlib(CompressedFileNames) <= 3.0.4-1
Requires(pre, post):   shadow-utils
BuildPrereq:    autoconf
Prereq:         coreutils
PreReq(post):          systemd
Prereq(pre,post):      coreutils
BuildPreReq(pre):      autoconf
OrderWithRequires(post): firewalld
OrderWithRequires(post,postun): firewalld
OrderWithRequires: firewalld

Provides:       %{name}-compat = %{version}-%{release}
Provides:       bundled(crate(serde)) = 1.0.200
  Provides:     indented-since-4-20
Obsoletes:      old-highlight-test < 1.0
Conflicts:      highlight-test-legacy
Recommends:     bash-completion
Recommends(meta): bash-completion-extras
Suggests(pre):    zed
Supplements(post): zed
Enhances(meta):   zed
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
%autosetup -n %{name}-%{version}
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
%define -e expanded_define %{major}.%{minor}
%define -g global_define value
%define -eg eg_define value
%dump
%trace
%trace
echo "after the broken macro lines"

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
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.{a,la}
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
# comment after a lua scriptlet

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
%doc docs/*.html

%if_enabled docs
%{_datadir}/%{name}/if-enabled-docs/
%endif

%changelog
* Thu Oct 29 2026 Its-J <jonah@fyralabs.com> - 2:1.27.0-1
- %%{excaped_macro}

* Wed Oct 28 2026 Its-J <jonah@fyralabs.com> - 2:1.26.0-2
- Epoch, version and release
- Update to 1.26.0 (rhbz#2222222, CVE-2026-12345, #11111)
- Fixes https://github.com/Its-J/rpmspec-zed/issues/1
  continuation line of the previous item
  - nested item
- Macro expanded in the changelog: %{version}
- Escaped macro: %%{name}

* Tue Oct 27 2026 Its-J <jonah@fyralabs.com> 1:1.25.0-1
- Version without the dash separator

* Mon Oct 26 2026 Its-J <jonah@fyralabs.com> - 1.24.0
- Version without a release

* Sun Oct 25 2026 Its-J <jonah@fyralabs.com>
- No version at all

* Sun Oct  4 2026 Its-J <jonah@fyralabs.com> - 1.23.0-1.fc45
- Single digit day padded with a space, release with a dist tag

* Sat Oct 3 2026 Its-J <jonah@fyralabs.com> - 1.22.0-0.1.20261003git1234abc
- Single digit day without padding, snapshot release

* Fri Oct  2 06:48:39 CEST 2026 Its-J <jonah@fyralabs.com> - 1.21.0-1
- Extended date format with time and timezone

* Thu Oct  1 23:59:59 UTC 2026 Its-J <jonah@fyralabs.com> - 1.20.0~rc1-1
- Extended date in UTC, tilde pre-release version

* Wed Sep 30 2026 jonah@fyralabs.com - 1.19.0-1
- Email only, no name

* Tue Sep 29 2026 Its-J - 1.18.0-1
- Name only, no email

* Mon Sep 28 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0^20260928git1234abc-2
- Multi word name, caret post-release snapshot version

%autochangelog
