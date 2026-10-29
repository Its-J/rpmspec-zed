# rpmspec-zed
RPM Spec Extension for Zed

must install perl and lua extentions for their highlighting injection to work

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
  - `ExcludeArch:`
  - `ExclusiveArch:`
  - `BuildArch:`
  - `Provides:       %{name}-compat = %{version}-%{release}` normal `Provides:` works but the provides in this one doesnt
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
