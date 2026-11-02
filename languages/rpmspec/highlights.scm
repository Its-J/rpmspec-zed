; Syntax highlighting queries for tree-sitter-rpmspec
;
; Organized following the structure of an RPM spec file:
; 1. Preamble (tags, dependencies)
; 2. Scriptlets (%prep, %build, %install, etc.)
; 3. Files section
; 4. Macros
; 5. Conditionals
; 6. Literals and operators

; =============================================================================
; PREAMBLE
; =============================================================================

; Tags like Name:, Version:, Release:, etc.
[
  (tag)
  (dependency_tag)
] @type.definition

; Dependency tag qualifier (e.g., post in Requires(post):)
(qualifier) @attribute.builtin

; Boolean dependency operators
[
  "if"
  "else"
  "unless"
  "with"
  "without"
] @keyword.operator

; Boolean dependency parentheses
(boolean_dependency
  "(" @punctuation.bracket
  ")" @punctuation.bracket)

; -----------------------------------------------------------------------------
; Dependency Types
; -----------------------------------------------------------------------------

; ELF dependencies: libc.so.6(GLIBC_2.2.5)(64bit)
(elf_dependency
  soname: (soname) @namespace @module
  symbol_version: (elf_symbol_version) @property
  arch: (elf_arch) @attribute)

; Path dependencies: /usr/bin/pkg-config
(path_dependency) @string.special.path

; Qualified dependencies: perl(Carp), pkgconfig(glib-2.0)
; LOCAL CHANGE: qualifier content (glib-2.0 in pkgconfig(glib-2.0)) is left
; uncolored, upstream tagged it @variable.parameter
(qualified_dependency
  name: (_) @function)

; ISA qualifiers override - known architecture patterns
((dependency_qualifier
   content: (word) @attribute)
 (#match? @attribute "^(x86-64|x86-32|aarch64|arm|ppc-64|ppc-32|s390x)$"))

; Simple dependencies: make, cmake-filesystem >= 3
; Note: qualified_dependency also has name field
(qualified_dependency
  name: (_) @namespace @module)
(dependency
  (word) @namespace @module)

; Source tag file paths
(preamble_tag
  value: (file) @string.special.path)

; Description and package sections
(description
  "%description" @keyword)
(package
  "%package" @keyword)

; Sourcelist section
(sourcelist
  "%sourcelist" @keyword)
(sourcelist
  (file) @string.special.path)

; Patchlist section
(patchlist
  "%patchlist" @keyword)
(patchlist
  (file) @string.special.path)

; =============================================================================
; SCRIPTLETS
; =============================================================================

; Build scriptlets (%prep, %build, %install, %check, %clean)
(prep_scriptlet
  (section_prep) @keyword)
(generate_buildrequires
  (section_generate_buildrequires) @keyword)
(conf_scriptlet
  (section_conf) @keyword)
(build_scriptlet
  (section_build) @keyword)
(install_scriptlet
  (section_install) @keyword)
(check_scriptlet
  (section_check) @keyword)
(clean_scriptlet
  (section_clean) @keyword)

; Runtime scriptlets (%pre, %post, %preun, %postun, etc.)
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
] @keyword

; Scriptlet interpreter (-p <program>)
(script_interpreter
  "-p" @variable.parameter)
(interpreter_program) @string.special.path

; Scriptlet augment options (-a, -p for append/prepend)
(scriptlet_augment_option) @variable.parameter

; Trigger scriptlets
[
  "%triggerprein"
  "%triggerin"
  "%triggerun"
  "%triggerpostun"
] @keyword

; File trigger scriptlets
[
  "%filetriggerin"
  "%filetriggerun"
  "%filetriggerpostun"
  "%transfiletriggerin"
  "%transfiletriggerun"
  "%transfiletriggerpostun"
] @keyword

; -----------------------------------------------------------------------------
; Prep macros (%setup, %autosetup, %patch, %autopatch)
; -----------------------------------------------------------------------------

; All prep macros use macro_option for their options via argument: field
[
  (setup_macro argument: (macro_option) @variable.parameter)
  (autosetup_macro argument: (macro_option) @variable.parameter)
  (autopatch_macro argument: (macro_option) @variable.parameter)
  (patch_macro argument: (macro_option) @variable.parameter)
]

; Patch number arguments
[
  (autopatch_macro (macro_argument) @number)
  (patch_macro (macro_argument) @number)
]

; =============================================================================
; FILES SECTION
; =============================================================================

(files
  "%files" @keyword)

; File directives
[
  "%artifact"
  "%attr"
  "%caps"
  "%config"
  "%defattr"
  "%dir"
  "%doc"
  "%docdir"
  "%exclude"
  "%ghost"
  "%license"
  "%missingok"
  "%readme"
] @keyword.type

; =============================================================================
; CHANGELOG
; =============================================================================

(changelog
  "%changelog" @keyword)

; =============================================================================
; MACROS
; =============================================================================

; -----------------------------------------------------------------------------
; Macro definitions
; -----------------------------------------------------------------------------

(macro_definition
  "%" @punctuation.special
  ["define" "global"] @constant.builtin
  name: (identifier) @keyword.macro)

(macro_undefinition
  "%" @punctuation.special
  (builtin) @constant.builtin
  (identifier) @keyword.macro)

; -----------------------------------------------------------------------------
; Simple macro expansion (%name, %!name, %*, etc.)
; -----------------------------------------------------------------------------

(macro_simple_expansion
  "%" @punctuation.special
  (simple_macro) @constant.macro)

(macro_simple_expansion
  "%" @punctuation.special
  (negated_macro) @constant.macro)

(macro_simple_expansion
  "%" @punctuation.special
  (special_macro) @constant.macro)

; -----------------------------------------------------------------------------
; Parametric macro expansion (%name [options] [arguments])
; -----------------------------------------------------------------------------

; Note: parametric_macro_name includes the '%' prefix and is aliased to simple_macro
(macro_parametric_expansion
  name: (identifier) @function.macro)

(macro_parametric_expansion
  option: (macro_option) @variable.parameter)

(macro_parametric_expansion
  argument: (word) @variable.parameter)

(macro_parametric_expansion
  argument: (integer) @number)

(macro_parametric_expansion
  argument: (quoted_string) @string)

; Macro options in parametric expansions
(macro_option) @variable.parameter

; -----------------------------------------------------------------------------
; Brace macro expansion (%{name}, %{name:arg}, etc.)
; -----------------------------------------------------------------------------

(macro_expansion
  "%{" @punctuation.special
  "}" @punctuation.special) @none

(macro_expansion
  (builtin) @constant.builtin
  argument: (_) @variable.parameter)

(macro_expansion
  (identifier) @constant.macro)

(macro_expansion
  (identifier)
  argument: [
    (word) @variable.parameter
    (concatenation
      (word) @variable.parameter)
  ])

; Conditional expansion (%{?name}, %{!?name})
(conditional_expansion
  condition: (identifier) @constant.macro)

; -----------------------------------------------------------------------------
; General macro rules
; -----------------------------------------------------------------------------

(special_variable_name) @constant
(builtin) @constant.builtin

; =============================================================================
; CONDITIONALS
; =============================================================================

; Conditional directives
[
  "%if"
  "%ifarch"
  "%ifnarch"
  "%ifos"
  "%ifnos"
  "%elif"
  "%elifarch"
  "%elifos"
  "%else"
  "%endif"
] @keyword.conditional

; Macro conditional operators
[
  "defined"
  "undefined"
] @keyword.operator

; =============================================================================
; LITERALS AND OPERATORS
; =============================================================================

; Numbers
(integer) @number
(float) @number.float
(version) @number.float

; Strings
(quoted_string) @string

; URLs
(url) @string.special.url

; Comments
(comment) @comment

; Comparison and logical operators
[
  "!="
  "<"
  "<="
  "="
  "=="
  ">"
  ">="
  "and"
  "&&"
  "or"
  "||"
] @operator

; =============================================================================
; LOCAL ADDITIONS (not in upstream tree-sitter-rpmspec)
; =============================================================================

; %{with foo} / %{defined foo} inside %if parse as operators, not macro_expansion
(with_operator
  "%{" @punctuation.special
  (identifier) @constant.macro
  "}" @punctuation.special)

(defined_operator
  "%{" @punctuation.special
  (identifier) @constant.macro
  "}" @punctuation.special)

; Arch/OS tag values: BuildArch: noarch, ExclusiveArch: x86_64 aarch64
((preamble_tag
  (dependency_tag) @_tag
  value: (word) @attribute)
  (#match? @_tag "(?i)^(BuildArch|BuildArchitectures|ExcludeArch|ExclusiveArch|ExcludeOS|ExclusiveOS):$"))

((preamble_tag
  (dependency_tag) @_tag
  value: (concatenation
    (word) @attribute))
  (#match? @_tag "(?i)^(BuildArch|BuildArchitectures|ExcludeArch|ExclusiveArch|ExcludeOS|ExclusiveOS):$"))

; Versioned dependency names: Provides: %{name}-compat = %{version}-%{release}
; (the name: field doesn't match the word here, so it's left off)
(version_dependency
  (word) @namespace @module)

; SPDX license expressions: MIT AND (Apache-2.0 OR BSD-3-Clause)
((word) @keyword.operator
  (#match? @keyword.operator "^(AND|OR|WITH)$"))

(parenthesized_expression
  [
    "("
    ")"
  ] @punctuation.bracket)

; Emails in Packager: and changelog headers: <john at example.com>
; The brackets are colored like macro punctuation, the address stays plain
; (needs the grammar fork, upstream has no email node)
(email
  "<" @punctuation.special
  ">" @punctuation.special)

; VCS values: VCS: git:https://github.com/... (the grammar parses them as words)
((preamble_tag
  (tag) @_tag
  value: (word) @string.special.url)
  (#match? @_tag "(?i)^vcs:$"))

; The % of the prep macros (%setup, %autosetup, %patch, %autopatch), upstream
; only colors their name and options
(setup_macro
  "%" @punctuation.special)

(autosetup_macro
  "%" @punctuation.special)

(patch_macro
  "%" @punctuation.special)

(autopatch_macro
  "%" @punctuation.special)

; Changelog entry headers: * Wed Oct 28 2026 Name <email> - 2:1.0-1
; (needs the grammar fork, upstream keeps the whole header as one string)
(changelog_entry
  "*" @punctuation.special)

(changelog_date) @constant

; The "-" before the version is colored like the version
(changelog_header
  "-" @number)

(changelog_version) @number

; Glob wildcards in %files paths: *, ?, [abc] (needs the grammar fork)
(glob) @string.regex

; The % of brace-less option references in parametric macros: %-f, %-f*
(macro_simple_expansion
  "%" @punctuation.special
  (macro_option))

; Inline %{dnl ...} comments: RPM drops everything inside, so grey all of it.
; These come last so they win over the macro colors above
((builtin) @comment
  (#eq? @comment "dnl"))

((macro_expansion
  "%{" @comment
  (builtin) @_dnl)
  (#eq? @_dnl "dnl"))

((macro_expansion
  (builtin) @_dnl
  _ @comment)
  (#eq? @_dnl "dnl"))

((macro_expansion
  (builtin) @_dnl
  (_
    _ @comment))
  (#eq? @_dnl "dnl"))

((macro_expansion
  (builtin) @_dnl
  (_
    (_
      _ @comment)))
  (#eq? @_dnl "dnl"))

; The modifier in %define name<l> / name<o> (rpm >= 6.1)
(macro_modifier) @attribute
