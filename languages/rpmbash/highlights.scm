; Syntax highlighting queries for tree-sitter-rpmbash
;
; rpmbash is tree-sitter-bash plus RPM macro nodes. It is only used as an
; injection for scriptlet bodies in RPM spec files, so it is hidden from the
; language picker.
;
; Based on tree-sitter-bash's queries/highlights.scm (MIT), using capture names
; from Zed's themes.
;
; RPM macros (%{name}, %name) and conditionals (%if/%endif) are deliberately not
; captured here: the parent rpmspec layer already highlights them, and leaving
; them uncaptured lets those highlights show through.

; =============================================================================
; LITERALS
; =============================================================================

[
  (string)
  (raw_string)
  (ansi_c_string)
  (translated_string)
  (heredoc_body)
  (heredoc_start)
  (heredoc_end)
] @string

(regex) @string.regex

[
  (number)
  (file_descriptor)
] @number

(comment) @comment

; =============================================================================
; COMMANDS
; =============================================================================

; Command names: make, install, sed, find, ...
(command_name
  (word) @function)

(function_definition
  name: (word) @function)

; Flags: -p, -Dpm, --prefix=/usr, ...
((command
  argument: (word) @constant)
  (#match? @constant "^-"))

((command
  argument: (concatenation
    .
    (word) @constant))
  (#match? @constant "^-"))

; =============================================================================
; VARIABLES
; =============================================================================

(variable_name) @variable

(special_variable_name) @variable.special

(simple_expansion
  "$" @punctuation.special)

(expansion
  "${" @punctuation.special
  "}" @punctuation.special)

(command_substitution
  "$(" @punctuation.special
  ")" @punctuation.special)

(arithmetic_expansion
  [
    "$(("
    "$["
    "))"
    "]"
  ] @punctuation.special)

; =============================================================================
; KEYWORDS
; =============================================================================

[
  "export"
  "function"
  "unset"
  "local"
  "declare"
  "readonly"
  "typeset"
] @keyword

[
  "case"
  "do"
  "done"
  "elif"
  "else"
  "esac"
  "fi"
  "for"
  "if"
  "in"
  "select"
  "then"
  "until"
  "while"
] @keyword

(test_operator) @operator

; =============================================================================
; OPERATORS AND PUNCTUATION
; =============================================================================

[
  "&&"
  "||"
  "|"
  "|&"
  "&"
  ">"
  ">>"
  ">&"
  ">&-"
  ">|"
  "&>"
  "&>>"
  "<"
  "<<"
  "<<-"
  "<<<"
  "<&"
  "<&-"
  "="
  "+="
  "=="
  "!="
  "=~"
  "!"
] @operator

[
  ";"
  ";;"
] @punctuation.delimiter

[
  "("
  ")"
  "(("
  "))"
  "["
  "]"
  "[["
  "]]"
] @punctuation.bracket

; Braces are listed per node so the "}" closing an RPM %{macro} stays
; uncaptured and keeps rpmspec's highlight.
(compound_statement
  [
    "{"
    "}"
  ] @punctuation.bracket)

(brace_expression
  [
    "{"
    "}"
  ] @punctuation.bracket)

; Glob patterns: *.la, docs/*.md (tree-sitter-bash has no glob node, so the
; whole word gets the color)
((word) @string.regex
  (#match? @string.regex "[*?]"))
