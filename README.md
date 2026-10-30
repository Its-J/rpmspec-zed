# rpmspec-zed
Extension that improves RedHat Package Manager .spec file support in Zed

# Installing

## From source (dev extension)
1. clone this repo
2. in zed, open the command palette and run `zed: install dev extension`
3. pick the cloned folder
   - zed clones the grammar repo and compiles it to wasm itself, so you only need `git` installed
   - after changing anything, hit `Rebuild` on it in the extensions panel (or install it again) to pick up the changes

## Prebuilt (no building)
the grammars compile to wasm, so a built copy works on any os

1. on a machine that already has it installed as a dev extension, copy these into a folder named `terra_rpmspec` (the `id` in `extension.toml`)
   ```
   terra_rpmspec/
   ├── extension.toml
   ├── languages/
   └── grammars/
       ├── rpmspec.wasm
       └── rpmbash.wasm
   ```
   - leave out `grammars/rpmspec/` and `grammars/rpmbash/`, those are just the grammar source checkouts
2. put that folder in zeds installed extensions folder
   - linux: `~/.local/share/zed/extensions/installed/`
   - macos: `~/Library/Application Support/Zed/extensions/installed/`
3. restart zed

## Scriptlet languages
scriptlets using `-p <lua>` or `-p /usr/bin/perl` only get highlighted if zed has those languages, and extensions cant install other extensions for you

- install the **Lua** and **Perl** extensions from the extensions panel
- python is built into zed, nothing extra needed
- bash scriptlets use the `rpmbash` grammar bundled with this extension

## Notes
- the `id` is `terra_rpmspec` because the zed registry already has a different extension with the id `rpmspec`, reusing that `id` could make zed swap this one for it
- only have one copy installed at a time, uninstall old dev installs from the extensions panel if the `id` changed

# Potential Issues
- [x] some sections dont get highlighted
  - build scriptlets: `%prep`, `%generate_buildrequires`, `%conf`, `%build`, `%install`, `%check`, `%clean`
  - runtime scriptlets: `%pre`, `%post`, `%preun`, `%postun`, `%pretrans`, `%posttrans`, `%preuntrans`, `%postuntrans`, `%verify`
  - triggers: `%triggerprein`, `%triggerin`, `%triggerun`, `%triggerpostun`
  - file triggers: `%filetriggerin`, `%filetriggerun`, `%filetriggerpostun`, `%transfiletriggerin`, `%transfiletriggerun`, `%transfiletriggerpostun`
  - they parse fine, but `highlights.scm` tags them all `@module.builtin`
  - zed themes have no `module` color, so they fall through to plain text
  - `%files`, `%changelog`, `%description`, `%package` work because theyre tagged `@type.definition`, which falls back to `type`
  - same thing hits `@module` on dependency names like `make` or `perl(Carp)`
  - fixed: every section header (scriptlets, triggers, `%package`, `%description`, `%files`, `%changelog`, `%sourcelist`, `%patchlist`) now uses `@keyword` so they all match
    - upstream split them on purpose: `@type.definition` for sections that describe the package, `@module.builtin` for sections that run code, neovim themes color those differently
    - in zed `@type` is also the color of every preamble tag (`Name:`, `Requires:`), so sections blended into tags, `@keyword` stands out in every theme
  - dependency names fall back to `@namespace` when the theme has no `module` color (`@namespace @module`)
- [ ] `%%{macro}` should get greyed out like a comment? maybe not idk
- [x] some tags break (grammar issue)
  - fixed in my fork of tree-sitter-rpmspec ([J-GitHubAcc/tree-sitter-rpmspec](https://gitlab.com/J-GitHubAcc/tree-sitter-rpmspec)), see `extension.toml`
  - [x] `BugURL:`, only `BugUrl:` works
    - fixed in the grammar fork, tag names are case insensitive now
  - [x] `Packager:` with an email, the `<` breaks it
    - confirmed, and the error eats the lines below it too, in the test spec `Distribution:`, `BugURL:`, `BuildArch:`, `ExclusiveArch:` and `ExcludeArch:` all lose their tag color
    - those lines all parse fine on their own, its just the `Packager:` error spilling over
    - fixed in the grammar fork, the email is its own `email` node, `<` and `>` get `@punctuation.special` and the address stays plain
  - [x] `Requires(post,postun):`, more than one qualifier
    - fixed in the grammar fork
  - [x] `OrderWithRequires(post):`, any qualifier
    - the error spills onto the next lines, so a plain `OrderWithRequires: firewalld` right after it breaks too
    - plain `OrderWithRequires:` works fine on its own
    - fixed in the grammar fork
  - [x] `Recommends(meta):`, weak deps (`Recommends`/`Suggests`/`Supplements`/`Enhances`) cant take a qualifier
    - the error eats every line below it until the next section, in the test spec thats `Suggests:`, `Enhances:`, `Supplements:` and `BuildConflicts:` all the way down to `%description`
    - fixed in the grammar fork, all four weak dep tags take qualifiers now
  - [x] lowercase tags like `buildrequires:`, rpm tags arent case sensitive but the grammar only knows the exact casing
    - fixed in the grammar fork
  - [x] `ExcludeArch:`, `ExclusiveArch:`, `BuildArch:` values werent highlighted
    - not a grammar issue, nothing colored the arch names, they now get `@attribute`
  - [x] `Provides:       %{name}-compat = %{version}-%{release}` normal `Provides:` works but the provides in this one doesnt
    - not a grammar issue, the name part of a versioned dependency had no highlight rule
- [x] some valid tags arent in the grammar at all (grammar issue)
  - `DistURL:`, `Icon:`, `TranslationUrl:`, `UpstreamReleases:`
  - `Requires(preuntrans):`, `Requires(postuntrans):`, the qualifier list stops at `posttrans`
  - one of these on its own is a local error, but a few together can turn the whole file into one big error
  - fixed in the grammar fork, all six are back in `tests/highlight-test.spec`
- [x] `%sourcelist`/`%patchlist` after the subpackages gets eaten by the last `%description`
  - the file lists under them get eaten too, they all show up as plain description text
  - its not caused by where they are, its caused by parse errors earlier in the file
    - with every broken line removed from the test spec (`Packager:` email, `BugURL:`, `buildrequires:`, `Requires(post,postun):`, `OrderWithRequires(post):`, `Recommends(meta):`) they parse fine right where they are
    - with any of those errors left above them, the error recovery leaves the last `%description` running over them
  - so fixing the tag bugs above would fix this too, putting them up with the `Source`/`Patch` tags also works around it
  - fixed: with the grammar fork the test spec has no parse errors, so they parse where they are
- [ ] `#` comments right after a `-p <lua>` scriptlet get highlighted as lua code
  - a scriptlet runs until the next section, so the comment is part of the lua script
  - the whole script gets injected as lua, and `#` isnt a comment in lua
  - rpm would run it as lua too, so its really a spec bug, not a highlighting one
  - use `--` comments in lua scriptlets, or put the comment after the next section header
- [x] macro option expansions dont parse (grammar issue)
  - `%{-n}`, `%{-f*}`, `%{-f:...}`, `%{?-n}`, `%{!?-n:...}`, `%-f`
  - the grammar only knows `%{name}`, it has no rule for a `-` option name
  - so stuff like `%{__cargo_parse_opts %{-n} %{-a} %{-f:-f%{-f*}}}` turns into errors
  - inside a `%global`/`%define` the error breaks the whole line
  - fixed in the grammar fork, all of those forms (and `%{!-f:...}`, nested ones) parse as `macro_option` now
  - the option gets `@variable.parameter` like `-n` in macro calls, `%{`/`}` and the `%` of `%-f` get `@punctuation.special`
  - `zed-nightly.spec` parses with no errors now
- [x] `AND` `OR` `(` `)` arent highlighted in `License:` tag
  - fixed: `AND`/`OR`/`WITH` get `@keyword.operator`, parens get `@punctuation.bracket`
- [x] `%{with foo}`, `%{without foo}`, `%{defined foo}`, `%{undefined foo}` inside `%if` dont look like other macros
  - in an `%if` the grammar parses them as `with_operator`/`defined_operator`, not `macro_expansion`
  - `highlights.scm` only colors `%{`, `}` and the name when the parent is `macro_expansion`
  - so only `with`/`defined` get colored (as `@keyword.operator`), the `%{`, `}` and `foo` stay plain
  - outside an `%if` (like `%global a %{with foo}`) they parse as normal macros and look fine
  - fixed: added patterns for `with_operator` and `defined_operator`
- [ ] `%{dnl ...}` doesnt get highlighted as a comment
  - `%{dnl:...}` and `%{dnl ...}` are inline comments, they only drop whats inside the braces
    - `a %{dnl x %{_bindir}} b` expands to `a  b`
  - `%{dnl}` on its own is an error (`%dnl: argument expected`)
  - the grammar parses the brace form as a normal builtin macro, so it gets macro colors
  - could add a pattern to `highlights.scm` to color it as `@comment`, but leaving it as is for now
- [x] preamble values turn the string color when a `%{lua:...}` macro with a macro inside it (like `rpm.expand("%{major}")`) is above them
  - the `%{lua:...}` injection rule used an `argument:` field, which only matched the first piece of lua before the inner macro
  - that piece ends in an open `"`, and zed merges every lua injection in the file into one layer, so the string ran until the next lua trigger hundreds of lines down
  - fixed: dropped the `argument:` field in `injections.scm` so every piece gets passed to lua
- [x] qualifier text like `glib-2.0` in `pkgconfig(glib-2.0)` was colored instead of white
  - fixed: removed upstreams `@variable.parameter` on the qualifier content, arch qualifiers like `x86-64` still get `@attribute`
- [x] `BuildRequires(pre):` doesnt parse (grammar issue)
  - the qualifier support only covers `Requires`, `OrderWithRequires` and the weak deps, not `BuildRequires`
  - seen in alt linux style specs
  - fixed in the grammar fork, `BuildRequires` takes the same qualifiers as `Requires` now
  - note: fedoras rpm (6.0.2) rejects this one with `Unknown tag`, its alt linux only, maybe leave it out of the upstream merge request
- [x] other qualifier forms rpm accepts but the grammar didnt (grammar issue)
  - `PreReq(post):` / `Prereq(post):` and `BuildPreReq(pre):`, deprecated but rpm still accepts them
  - `Requires(rpmlib):`, `rpmlib` was missing from the qualifier list
  - checked against `rpmspec` 6.0.2, qualifiers on `Provides`, `Conflicts`, `Obsoletes` and `BuildConflicts` are rejected by rpm too, so those stay unsupported
  - fixed in the grammar fork
- [ ] `%autochangelog` followed by normal changelog entries breaks (grammar issue)
  - `%autochangelog` on its own in `%changelog` is fine, but any `* date name - version` entries after it turn into a parse error
  - it ends the changelog for the grammar, so every entry after it breaks
  - left out of `tests/highlight-test.spec` so its 12 changelog entries still highlight
- [ ] `%if_enabled foo` ... `%endif` breaks (grammar issue)
  - `%if_enabled` is an alt linux macro that expands to an `%if`, the grammar only sees a normal macro call so the `%endif` has no matching `%if`
  - same goes for any distro macro that expands to a conditional
- [x] add highlighting for metadata in changelog like * - VERSION-RELEASE, timezone, etc
  - fixed in the grammar fork, entry headers are split into `changelog_date`, `changelog_author`, `email` and `changelog_version` instead of one string
  - `*` gets `@punctuation.special`, the date (with time and timezone) `@constant`, the `-` and version `@number`, the author stays plain
  - the email is colored the same as in `Packager:`, `<` and `>` get `@punctuation.special` and the address stays plain
  - headers that dont fit (no valid date) fall back to plain text instead of erroring
- [x] catchalls like * in %files and elsewhere should get their own highlighting not sure what though
  - fixed in the grammar fork, `*`, `?` and `[abc]` in `%files` paths (including inside `{,.*}`) are their own `glob` node now, colored `@string.regex`
  - escaped `\*` and quoted paths like `"/opt/a *"` stay plain, rpm doesnt glob those
  - not done in scriptlets, `rm -f *.la` in `%install` is bash, and tree-sitter-bash has no glob node to color
- [x] the `%` in `%setup`, `%autosetup`, `%patch` and `%autopatch` was white instead of red like other macros
  - upstream only colored their name and options, added `@punctuation.special` for their `%`
- [ ] `%define -e`, `%define -g` and `%define -eg` dont parse (grammar issue)
  - new options in rpm 6.1 (expand body now / define globally), rpm 6.0.2 rejects them too
  - left out of `tests/highlight-test.spec`
- [ ] macro modifiers `%define foo<l> ...` and `%define foo<o> ...` parse as plain words
  - literal and one-shot macros, new in rpm 6.1
  - no parse error, but the `<l>`/`<o>` dont get their own highlighting
- [ ] brace-less `%dump` and `%trace` on their own line break the parse (grammar issue)
  - `%{dump}` and `%{trace}` work fine, the test spec uses those
- [ ] change the extension id to rpmspec before contributing to zed registry

# Credits
- syntax highlighting is powered by [tree-sitter-rpmspec](https://gitlab.com/cryptomilk/tree-sitter-rpmspec) by Andreas Schneider ([cryptomilk](https://gitlab.com/cryptomilk))
  - both the `rpmspec` and `rpmbash` grammars come from it
  - `languages/rpmspec/highlights.scm` and `injections.scm` are copied from its `rpmspec/queries/`
