graph [
  directed 1
  node [
    id 0
    label "1"
    pos 56
    pos 254
    name "switch"
    data "switch"
  ]
  node [
    id 1
    label "2"
    pos 99
    pos 256
    name "_"
    data " "
  ]
  node [
    id 2
    label "3"
    pos 140
    pos 256
    name "("
    data "("
  ]
  node [
    id 3
    label "4"
    pos 184
    pos 258
    name "expression"
    data "expression"
  ]
  node [
    id 4
    label "5"
    pos 238
    pos 259
    name ")"
    data ")"
  ]
  node [
    id 5
    label "6"
    pos 280
    pos 258
    name "\n"
    data "\n"
  ]
  node [
    id 6
    label "7"
    pos 326
    pos 262
    name "{"
    data "{"
  ]
  node [
    id 7
    label "8"
    pos 519
    pos 321
    name "switch_block"
    data "switch_block"
  ]
  node [
    id 8
    label "9"
    pos 388
    pos 295
    name "increase_offset"
    data "increase_offset"
  ]
  node [
    id 9
    label "10"
    pos 593
    pos 327
    name "decrease_offset"
    data "decrease_offset"
  ]
  node [
    id 10
    label "11"
    pos 679
    pos 329
    name "}"
    data "}"
  ]
  node [
    id 11
    label "12"
    pos 446
    pos 321
    name "\n"
    data "\n"
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
