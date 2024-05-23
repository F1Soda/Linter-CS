graph [
  directed 1
  node [
    id 0
    label "0"
    pos 137
    pos 247
    name "try"
    data "try"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 135
    pos 371
    name "finally"
    data "finally"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 126
    pos 496
    name "catch"
    data "catch"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 214
    pos 310
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 332
    pos 306
    name "just_block"
    data "just_block"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 208
    pos 495
    name "check_()_in_catch"
    data "check_()_in_catch"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 297
    pos 507
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 381
    pos 508
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 454
    pos 510
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 514
    pos 509
    name ")"
    data ")"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 3
    condition "default"
  ]
  edge [
    source 1
    target 3
    condition "default"
  ]
  edge [
    source 2
    target 5
    condition "default"
  ]
  edge [
    source 3
    target 4
    condition "default"
  ]
  edge [
    source 5
    target 3
    condition "False"
  ]
  edge [
    source 5
    target 6
    condition "True"
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
    source 9
    target 3
    condition "default"
  ]
]
