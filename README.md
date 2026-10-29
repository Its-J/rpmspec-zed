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
- some sections dont get highlighted
  - build scriptlets: `%prep`, `%generate_buildrequires`, `%conf`, `%build`, `%install`, `%check`, `%clean`
  - runtime scriptlets: `%pre`, `%post`, `%preun`, `%postun`, `%pretrans`, `%posttrans`, `%preuntrans`, `%postuntrans`, `%verify`
  - triggers: `%triggerprein`, `%triggerin`, `%triggerun`, `%triggerpostun`
  - file triggers: `%filetriggerin`, `%filetriggerun`, `%filetriggerpostun`, `%transfiletriggerin`, `%transfiletriggerun`, `%transfiletriggerpostun`
  - they parse fine, but `highlights.scm` tags them all `@module.builtin`
  - zed themes have no `module` color, so they fall through to plain text
  - `%files`, `%changelog`, `%description`, `%package` work because theyre tagged `@type.definition`, which falls back to `type`
  - same thing hits `@module` on dependency names like `make` or `perl(Carp)`
  - fix is swapping those captures for a name zed themes have, like `@keyword` or `@type`
- `%%{macro}` should get greyed out like a comment? maybe not idk
- some tags break (grammar issue)
  - `BugURL:`, only `BugUrl:` works
  - `Packager:` with an email, the `<` breaks it? maybe not idk
  - `Requires(post,postun):`, more than one qualifier
  - `OrderWithRequires(post):`, any qualifier
    - the error spills onto the next lines, so a plain `OrderWithRequires: firewalld` right after it breaks too
    - plain `OrderWithRequires:` works fine on its own
  - `Recommends(meta):`, weak deps (`Recommends`/`Suggests`/`Supplements`/`Enhances`) cant take a qualifier
    - the error eats every line below it until the next section, in the test spec thats `Suggests:`, `Enhances:`, `Supplements:` and `BuildConflicts:` all the way down to `%description`
  - lowercase tags like `buildrequires:`, rpm tags arent case sensitive but the grammar only knows the exact casing
  - `ExcludeArch:`
  - `ExclusiveArch:`
  - `BuildArch:`
  - `Provides:       %{name}-compat = %{version}-%{release}` normal `Provides:` works but the provides in this one doesnt
- some valid tags arent in the grammar at all (grammar issue)
  - `DistURL:`, `Icon:`, `TranslationUrl:`, `UpstreamReleases:`
  - `Requires(preuntrans):`, `Requires(postuntrans):`, the qualifier list stops at `posttrans`
  - one of these on its own is a local error, but a few together can turn the whole file into one big error
  - left them out of `tests/highlight-test.spec` so the rest of it still highlights
- `%sourcelist`/`%patchlist` after the subpackages gets eaten by the last `%description`
  - works if its put up with the `Source`/`Patch` tags
- `#` comments right after a `-p <lua>` scriptlet get highlighted as lua code
  - a scriptlet runs until the next section, so the comment is part of the lua script
  - the whole script gets injected as lua, and `#` isnt a comment in lua
  - rpm would run it as lua too, so its really a spec bug, not a highlighting one
  - use `--` comments in lua scriptlets, or put the comment after the next section header
- macro option expansions dont parse (grammar issue)
  - `%{-n}`, `%{-f*}`, `%{-f:...}`, `%{?-n}`, `%{!?-n:...}`, `%-f`
  - the grammar only knows `%{name}`, it has no rule for a `-` option name
  - so stuff like `%{__cargo_parse_opts %{-n} %{-a} %{-f:-f%{-f*}}}` turns into errors
  - inside a `%global`/`%define` the error breaks the whole line
- `AND` `OR` `(` `)` arent highlighted in `License:` tag
- `%{with foo}`, `%{without foo}`, `%{defined foo}`, `%{undefined foo}` inside `%if` dont look like other macros
  - in an `%if` the grammar parses them as `with_operator`/`defined_operator`, not `macro_expansion`
  - `highlights.scm` only colors `%{`, `}` and the name when the parent is `macro_expansion`
  - so only `with`/`defined` get colored (as `@keyword.operator`), the `%{`, `}` and `foo` stay plain
  - outside an `%if` (like `%global a %{with foo}`) they parse as normal macros and look fine
  - fix is adding patterns for `with_operator` and `defined_operator` to `highlights.scm`
- `%{dnl ...}` doesnt get highlighted as a comment
  - `%{dnl:...}` and `%{dnl ...}` are inline comments, they only drop whats inside the braces
    - `a %{dnl x %{_bindir}} b` expands to `a  b`
  - `%{dnl}` on its own is an error (`%dnl: argument expected`)
  - the grammar parses the brace form as a normal builtin macro, so it gets macro colors
  - could add a pattern to `highlights.scm` to color it as `@comment`, but leaving it as is for now
- change the extension id to rpmspec before contributing to zed registry

# Credits
- syntax highlighting is powered by [tree-sitter-rpmspec](https://gitlab.com/cryptomilk/tree-sitter-rpmspec) by Andreas Schneider ([cryptomilk](https://gitlab.com/cryptomilk)), MIT licensed
  - both the `rpmspec` and `rpmbash` grammars come from it
  - `languages/rpmspec/highlights.scm` and `injections.scm` are copied from its `rpmspec/queries/`
