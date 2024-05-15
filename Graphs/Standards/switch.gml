graph [
  directed 1
  node [
    id 0
    label "0"
    pos 56
    pos 254
    name "switch"
    data "switch"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 99
    pos 256
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 140
    pos 256
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 184
    pos 258
    name "expression"
    data "expression"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 238
    pos 259
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 280
    pos 258
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 326
    pos 262
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 519
    pos 321
    name "switch_block"
    data "switch_block"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 388
    pos 295
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 593
    pos 327
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 10
    label "10"
    pos 679
    pos 329
    name "}"
    data "}"
    should_check_offset "default"
  ]
  node [
    id 11
    label "11"
    pos 446
    pos 321
    name "\n"
    data "\n"
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
  edge [
    source 6
    target 8
  ]
  edge [
    source 7
    target 9
  ]
  edge [
    source 8
    target 11
  ]
  edge [
    source 9
    target 10
  ]
  edge [
    source 11
    target 7
  ]
]
