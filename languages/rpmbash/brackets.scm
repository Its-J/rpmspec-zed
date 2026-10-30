; Bracket pairs for matching and jumping between brackets in scriptlets

("(" @open ")" @close)
("[" @open "]" @close)
("{" @open "}" @close)
("[[" @open "]]" @close)
("((" @open "))" @close)
("\"" @open "\"" @close)

; $(cmd), $((math)), ${var}, <(cmd), >(cmd)
("$(" @open ")" @close)
("$((" @open "))" @close)
("${" @open "}" @close)
("<(" @open ")" @close)
(">(" @open ")" @close)

; RPM macros inside scriptlets: %{name}
(rpm_macro_expansion
  "%{" @open
  "}" @close)

; Keyword blocks
(if_statement
  "if" @open
  "fi" @close)

(case_statement
  "case" @open
  "esac" @close)

(do_group
  "do" @open
  "done" @close)
