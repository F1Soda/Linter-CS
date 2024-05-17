graph [
  directed 1
  node [
    id 0
    label "0"
    pos 61
    pos 230
    name "do"
    data "do"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 123
    pos 230
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 2
    label "2"
    pos 118
    pos 342
    name "while"
    data "while"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 171
    pos 338
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 226
    pos 337
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 292
    pos 339
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 361
    pos 343
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 419
    pos 343
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 258
    pos 221
    name "line_or_block"
    data "line_or_block"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 50
    pos 342
    name "_"
    data " "
    should_check_offset "default"
  ]
  edge [
    source 0
    target 1
    condition "default"
  ]
  edge [
    source 1
    target 8
    condition "default"
  ]
  edge [
    source 2
    target 3
    condition "default"
  ]
  edge [
    source 3
    target 4
    condition "default"
  ]
  edge [
    source 4
    target 5
    condition "default"
  ]
  edge [
    source 5
    target 6
    condition "default"
  ]
  edge [
    source 6
    target 7
    condition "default"
  ]
  edge [
    source 8
    target 9
    condition "False"
  ]
  edge [
    source 8
    target 2
    condition "True"
  ]
  edge [
    source 9
    target 2
    condition "default"
  ]
]
