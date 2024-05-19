graph [
  directed 1
  node [
    id 0
    label "0"
    pos 104
    pos 320
    name "for"
    data "for"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 174
    pos 321
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 226
    pos 322
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 379
    pos 318
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 441
    pos 288
    name "expression_;_skip_first"
    data "expression_;_skip_first"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 510
    pos 325
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 590
    pos 285
    name "expression_)_skip_first"
    data "expression_)_skip_first"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 757
    pos 364
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 157
    pos 363
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 9
    label "9"
    pos 228
    pos 404
    name "line_or_block"
    data "line_or_block"
    should_check_offset "default"
  ]
  node [
    id 10
    label "10"
    pos 303
    pos 290
    name "expression_;_skip_first"
    data "expression_;_skip_first"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 1
    condition "default"
  ]
  edge [
    source 1
    target 2
    condition "default"
  ]
  edge [
    source 2
    target 10
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
    source 7
    target 8
    condition "default"
  ]
  edge [
    source 8
    target 9
    condition "default"
  ]
  edge [
    source 10
    target 3
    condition "default"
  ]
]
