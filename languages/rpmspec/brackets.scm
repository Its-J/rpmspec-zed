; Bracket pairs for matching and jumping between brackets
;
; Not matched: the "(" in Requires(post): and %config(...) is part of the tag
; token itself, so there is no separate open bracket to pair with.

; Macros: %{name}, %(shell), %[expression]
("%{" @open "}" @close)
("%(" @open ")" @close)
("%[" @open "]" @close)

; Parentheses: boolean dependencies, pkgconfig(foo), %attr(...), %define name(opts),
; parenthesized expressions
("(" @open ")" @close)

; Brace expansion in %files paths: {a,b}
(brace_expansion
  "{" @open
  "}" @close)

; Emails: <john at example.com>
(email
  "<" @open
  ">" @close)

; Strings: "value", v"1.0-1"
("\"" @open "\"" @close)

; Conditionals, only for the named statement nodes; the hidden variants are
; folded into their parent where several blocks would be siblings
(if_statement
  "%if" @open
  "%endif" @close)

(ifarch_statement
  [
    "%ifarch"
    "%ifnarch"
  ] @open
  "%endif" @close)

(ifos_statement
  [
    "%ifos"
    "%ifnos"
  ] @open
  "%endif" @close)
