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
    pos 130
    pos 230
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 2
    label "10"
    pos 117
    pos 334
    name "while"
    data "while"
    should_check_offset "default"
  ]
  node [
    id 3
    label "11"
    pos 171
    pos 338
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 4
    label "12"
    pos 226
    pos 337
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 5
    label "13"
    pos 292
    pos 339
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 6
    label "14"
    pos 360
    pos 343
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 7
    label "15"
    pos 419
    pos 343
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 8
    label "117"
    pos 244
    pos 227
    name "line_or_block"
    data "line_or_block"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 8
  ]
  edge [
    source 2
    target 3
  ]
  edge [
    source 3
    target 4
  ]
  edge [
    source 4
    target 5
  ]
  edge [
    source 5
    target 6
  ]
  edge [
    source 6
    target 7
  ]
  edge [
    source 8
    target 2
  ]
]
