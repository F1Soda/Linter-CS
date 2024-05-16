graph [
  directed 1
  node [
    id 0
    label "0"
    pos 35
    pos 187
    name "case"
    data "case"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 114
    pos 245
    name "default"
    data "default"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 182
    pos 187
    name ":"
    data ":"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 303
    pos 184
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 240
    pos 225
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 384
    pos 193
    name "case_block"
    data "case_block"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 454
    pos 146
    name "break"
    data "break"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 578
    pos 185
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 411
    pos 258
    name "return"
    data "return"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 529
    pos 248
    name "expression"
    data "expression"
    should_check_offset "default"
  ]
  node [
    id 10
    label "10"
    pos 120
    pos 186
    name "expression_:"
    data "expression_:"
    should_check_offset "default"
  ]
  node [
    id 11
    label "11"
    pos 647
    pos 185
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 12
    label "12"
    pos 75
    pos 187
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 13
    label "13"
    pos 475
    pos 265
    name "_"
    data " "
    should_check_offset "default"
  ]
  edge [
    source 0
    target 12
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 2
    target 4
  ]
  edge [
    source 3
    target 5
  ]
  edge [
    source 4
    target 3
  ]
  edge [
    source 5
    target 6
  ]
  edge [
    source 5
    target 8
  ]
  edge [
    source 6
    target 7
  ]
  edge [
    source 7
    target 11
  ]
  edge [
    source 8
    target 13
  ]
  edge [
    source 9
    target 7
  ]
  edge [
    source 10
    target 2
  ]
  edge [
    source 12
    target 10
  ]
  edge [
    source 13
    target 9
  ]
]
