graph [
  directed 1
  node [
    id 0
    label "1"
    pos 139
    pos 340
    name "if"
    data "if"
  ]
  node [
    id 1
    label "2"
    pos 178
    pos 342
    name "_"
    data " "
  ]
  node [
    id 2
    label "3"
    pos 220
    pos 342
    name "("
    data "("
  ]
  node [
    id 3
    label "4"
    pos 260
    pos 344
    name "expression"
    data "expression"
  ]
  node [
    id 4
    label "5"
    pos 300
    pos 342
    name ")"
    data ")"
  ]
  node [
    id 5
    label "6"
    pos 360
    pos 305
    name "\n"
    data "\n"
  ]
  node [
    id 6
    label "7"
    pos 410
    pos 345
    name "{"
    data "{"
  ]
  node [
    id 7
    label "8"
    pos 469
    pos 433
    name "block"
    data "block"
  ]
  node [
    id 8
    label "9"
    pos 414
    pos 506
    name "}"
    data "}"
  ]
  node [
    id 9
    label "10"
    pos 493
    pos 303
    name "line"
    data "line"
  ]
  node [
    id 10
    label "11"
    pos 412
    pos 303
    name "increase_offset"
    data "increase_offset"
  ]
  node [
    id 11
    label "12"
    pos 565
    pos 303
    name "decrease_offset"
    data "decrease_offset"
  ]
  node [
    id 12
    label "13"
    pos 583
    pos 395
    name "increase_offset"
    data "increase_offset"
  ]
  node [
    id 13
    label "14"
    pos 470
    pos 475
    name "decrease_offset"
    data "decrease_offset"
  ]
  node [
    id 14
    label "15"
    pos 464
    pos 348
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
    source 4
    target 6
  ]
  edge [
    source 5
    target 6
  ]
  edge [
    source 5
    target 10
  ]
  edge [
    source 6
    target 14
  ]
  edge [
    source 7
    target 13
  ]
  edge [
    source 9
    target 11
  ]
  edge [
    source 10
    target 9
  ]
  edge [
    source 12
    target 7
  ]
  edge [
    source 13
    target 8
  ]
  edge [
    source 14
    target 12
  ]
]
