graph [
  directed 1
  node [
    id 0
    label "0"
    pos 20
    pos 88
    name "else"
    data "else"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 53
    pos 276
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 2
    label "2"
    pos 80
    pos 151
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 157
    pos 152
    name "if"
    data "if"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 241
    pos 141
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 374
    pos 142
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 451
    pos 141
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 308
    pos 142
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 139
    pos 311
    name "line_or_block"
    data "line_or_block"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 2
    condition "default"
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
    target 7
    condition "default"
  ]
  edge [
    source 5
    target 6
    condition "default"
  ]
  edge [
    source 6
    target 1
    condition "default"
  ]
  edge [
    source 7
    target 5
    condition "default"
  ]
]
