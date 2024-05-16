graph [
  directed 1
  node [
    id 0
    label "0"
    pos 110
    pos 341
    name "if"
    data "if"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 178
    pos 342
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 220
    pos 342
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 260
    pos 344
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 305
    pos 334
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 5
    label "13"
    pos 356
    pos 353
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 6
    label "17"
    pos 423
    pos 340
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
    target 2
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
]
