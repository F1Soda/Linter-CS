graph [
  node [
    id 0
    label "1"
    pos 140
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
    pos 416
    pos 342
    name "{"
    data "{"
  ]
  node [
    id 7
    label "8"
    pos 450
    pos 344
    name "block"
    data "block"
  ]
  node [
    id 8
    label "9"
    pos 486
    pos 344
    name "}"
    data "}"
  ]
  node [
    id 9
    label "10"
    pos 414
    pos 305
    name "line"
    data "line"
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
    target 9
  ]
  edge [
    source 6
    target 7
  ]
  edge [
    source 7
    target 8
  ]
]
