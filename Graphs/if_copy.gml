graph [
  directed 1
  node [
    id 0
    label "1"
    pos 83
    pos 339
    name "if"
    data "if"
  ]
  node [
    id 1
    label "2"
    pos 133
    pos 339
    name "_"
    data " "
  ]
  node [
    id 2
    label "3"
    pos 172
    pos 334
    name "("
    data "("
  ]
  node [
    id 3
    label "4"
    pos 249
    pos 446
    name "expression"
    data "expression"
  ]
  node [
    id 4
    label "5"
    pos 319
    pos 341
    name ")"
    data ")"
  ]
  node [
    id 5
    label "6"
    pos 362
    pos 257
    name "\n"
    data "\n"
  ]
  node [
    id 6
    label "7"
    pos 409
    pos 341
    name "{"
    data "{"
  ]
  node [
    id 7
    label "8"
    pos 479
    pos 428
    name "block"
    data "block"
  ]
  node [
    id 8
    label "9"
    pos 563
    pos 361
    name "}"
    data "}"
  ]
  node [
    id 9
    label "10"
    pos 470
    pos 257
    name "line"
    data "line"
  ]
  node [
    id 10
    label "11"
    pos 193
    pos 395
    name "_"
    data "_"
  ]
  node [
    id 11
    label "12"
    pos 295
    pos 392
    name "_"
    data "_"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 0
  ]
  edge [
    source 1
    target 2
  ]
  edge [
    source 2
    target 1
  ]
  edge [
    source 2
    target 10
  ]
  edge [
    source 3
    target 11
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
    target 4
  ]
  edge [
    source 5
    target 9
  ]
  edge [
    source 5
    target 6
  ]
  edge [
    source 6
    target 4
  ]
  edge [
    source 6
    target 7
  ]
  edge [
    source 7
    target 6
  ]
  edge [
    source 7
    target 8
  ]
  edge [
    source 8
    target 7
  ]
  edge [
    source 9
    target 5
  ]
  edge [
    source 10
    target 3
  ]
  edge [
    source 11
    target 4
  ]
]
