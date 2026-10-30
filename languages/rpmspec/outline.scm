; Outline: shown in the outline panel and used for symbol search
;
; @item is the whole entry, @name the searchable label, @context extra text
; shown next to it (both in source order)

; Package name
((preamble_tag
  (tag) @context
  value: (_) @name) @item
  (#match? @context "(?i)^name:$"))

; Macro definitions: %global name, %define name(opts)
(macro_definition
  [
    "define"
    "global"
  ] @context
  name: (_)+ @name) @item

; Subpackages and their sections: %package devel, %description -n python3-foo
; A name like python3-%{name} is several name: fields, so all of them are captured
(package
  "%package" @name
  "-n"? @context
  name: (_)+ @name) @item

(description
  "%description" @name
  "-n"? @context
  name: (_)* @name) @item

(files
  "%files" @name
  "-n"? @context
  name: (_)* @name) @item

(sourcelist
  "%sourcelist" @name) @item

(patchlist
  "%patchlist" @name) @item

; Build scriptlets: %prep, %build, %build -a, ...
(prep_scriptlet
  (section_prep) @name) @item

(generate_buildrequires
  (section_generate_buildrequires) @name) @item

(conf_scriptlet
  (section_conf) @name
  (scriptlet_augment_option)? @context) @item

(build_scriptlet
  (section_build) @name
  (scriptlet_augment_option)? @context) @item

(install_scriptlet
  (section_install) @name
  (scriptlet_augment_option)? @context) @item

(check_scriptlet
  (section_check) @name
  (scriptlet_augment_option)? @context) @item

(clean_scriptlet
  (section_clean) @name) @item

; Runtime scriptlets: %post, %post devel, %pretrans -p <lua>
(runtime_scriptlet
  [
    "%pre"
    "%post"
    "%preun"
    "%postun"
    "%pretrans"
    "%posttrans"
    "%preuntrans"
    "%postuntrans"
    "%verify"
  ] @name
  "-n"? @context
  name: (_)* @name) @item

(runtime_scriptlet_interpreter
  [
    "%pre"
    "%post"
    "%preun"
    "%postun"
    "%pretrans"
    "%posttrans"
    "%preuntrans"
    "%postuntrans"
    "%verify"
  ] @name
  "-n"? @context
  name: (_)* @name
  interpreter: (script_interpreter) @context) @item

; Triggers: %triggerin -- zed, %filetriggerin -- /usr/lib
(trigger
  type: _ @name
  subpackage: (trigger_subpackage)? @name
  condition: (trigger_condition)? @context) @item

(file_trigger
  type: _ @name
  paths: (file_trigger_paths)? @context) @item

; Changelog, with each entry nested under it by date and version
(changelog
  "%changelog" @name) @item

(changelog_entry
  (changelog_header
    date: (changelog_date) @name
    version: (changelog_version)? @context)) @item
