# rpmspec-zed
Extension that improves RedHat Package Manager .spec file support in Zed

# Installation

## Dependencies
- [rpm-spec-language-server](https://github.com/dcermak/rpm-spec-language-server) for completion, hover and go to definition: `sudo dnf install rpm-spec-language-server`
- install the Lua and Perl extensions to get highlighting in `-p <lua>` and `-p /usr/bin/perl` scriptlets

## From source (dev extension)
1. clone this repo
2. in zed, run `zed: install dev extension` from the command palette (`Ctrl + Shift + P`) and pick the cloned folder
   - zed clones the grammar and compiles it itself, you need `git` and rust installed through rustup (`sudo dnf install rustup` then `rustup-init`)
   - after changing anything hit `Rebuild` in the extensions panel
   - if rebuild says the grammar dir "is not a git clone", delete `grammars/` and rebuild

## Prebuilt (no building)
1. on a machine with it installed as a dev extension, copy this into a folder named `terra_rpmspec`
   ```
   terra_rpmspec/
   ├── extension.toml
   ├── extension.wasm
   ├── languages/
   └── grammars/
       ├── rpmspec.wasm
       └── rpmbash.wasm
   ```
2. put that folder in zeds installed extensions folder `~/.local/share/zed/extensions/installed/`
3. restart zed

# Known Issues
- [ ] globs in scriptlets like `rm -f *.la` color the whole word, not just the `*`, tree-sitter-bash has no glob node
- [ ] change the extension id to rpmspec before contributing to zed registry

# Credits
- the grammars come from [tree-sitter-rpmspec](https://gitlab.com/cryptomilk/tree-sitter-rpmspec) by Andreas Schneider ([cryptomilk](https://gitlab.com/cryptomilk))
  - this extension uses [my fork](https://gitlab.com/J-GitHubAcc/tree-sitter-rpmspec) with grammar fixes
  - `languages/rpmspec/highlights.scm` and `injections.scm` started as copies of its queries
- `src/lib.rs` (the language server setup) is based on [zed-rpmspec-language](https://github.com/mtorromeo/zed-rpmspec-language) by Massimiliano Torromeo
- `languages/rpmbash/highlights.scm` is based on [tree-sitter-bash](https://github.com/tree-sitter/tree-sitter-bash)s queries
