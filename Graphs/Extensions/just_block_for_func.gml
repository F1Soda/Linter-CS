graph [
  directed 1
  node [
    id 0
    label "0"
    pos 252
    pos 274
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 309
    pos 274
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 447
    pos 275
    name "block"
    data "block"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 573
    pos 277
    name "}"
    data "}"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 375
    pos 273
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 515
    pos 275
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 414
    pos 306
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 1
    condition "default"
  ]
  edge [
    source 1
    target 4
    condition "default"
  ]
  edge [
    source 2
    target 5
    condition "default"
  ]
  edge [
    source 4
    target 6
    condition "default"
  ]
  edge [
    source 5
    target 3
    condition "default"
  ]
  edge [
    source 6
    target 2
    condition "default"
  ]
]
