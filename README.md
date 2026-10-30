# `rpmspec-zed`
Extension that improves RedHat Package Manager .spec file support in Zed

# Installation

## From source (dev extension)
1. clone this repo
2. in zed, run `zed: install dev extension` from the command palette (`Ctrl + Shift + P`) and pick the cloned folder
   - zed clones the grammar and compiles it itself, you only need `git`
   - after changing anything hit `Rebuild` in the extensions panel
   - if rebuild says the grammar dir "is not a git clone", delete `grammars/` and rebuild

## Prebuilt (no building)
1. on a machine with it installed as a dev extension, copy this into a folder named `terra_rpmspec`
   ```
   terra_rpmspec/
   ├── extension.toml
   ├── languages/
   └── grammars/
       ├── rpmspec.wasm
       └── rpmbash.wasm
   ```
2. put that folder in zeds installed extensions folder
   - linux: `~/.local/share/zed/extensions/installed/`
   - macos: `~/Library/Application Support/Zed/extensions/installed/`
3. restart zed

## Scriptlet languages
- install the Lua and Perl extensions to get highlighting in `-p <lua>` and `-p /usr/bin/perl` scriptlets
- python is built into zed
- bash scriptlets use the `rpmbash` grammar that comes with this extension

## Notes
- the id is `terra_rpmspec` because the zed registry already has an `rpmspec` extension
- only keep one copy installed, uninstall old dev installs if the id changed

# Known Issues
- [ ] `%%{macro}` should get greyed out like a comment? maybe not idk
- [ ] `#` comments right after a `-p <lua>` scriptlet get highlighted as lua
  - the comment is part of the lua script until the next section, and `#` isnt a lua comment
  - rpm runs it as lua too, so use `--` comments in lua scriptlets
- [ ] inline `%{dnl ...}` doesnt get highlighted as a comment
- [ ] `%autochangelog` followed by normal changelog entries breaks
- [ ] `%if_enabled foo` ... `%endif` breaks
  - alt linux macro that expands to an `%if`, the grammar cant know that
- [ ] `%define -e`, `-g` and `-eg` dont parse
- [ ] `%define foo<l>` / `foo<o>` modifiers parse as plain words
- [ ] `%dump` and `%trace` without braces break the parse
- [ ] globs like `rm -f *.la` in scriptlets arent highlighted, tree-sitter-bash has nothing to color
- [ ] `%description -n python3-%{name}` shows as `python3-` in the outline
- [ ] change the extension id to rpmspec before contributing to zed registry

# Credits
- the grammars come from [tree-sitter-rpmspec](https://gitlab.com/cryptomilk/tree-sitter-rpmspec) by Andreas Schneider ([cryptomilk](https://gitlab.com/cryptomilk))
  - this extension uses [my fork](https://gitlab.com/J-GitHubAcc/tree-sitter-rpmspec) with grammar fixes
  - `languages/rpmspec/highlights.scm` and `injections.scm` started as copies of its queries
- `languages/rpmbash/highlights.scm` is based on [tree-sitter-bash](https://github.com/tree-sitter/tree-sitter-bash)s queries
