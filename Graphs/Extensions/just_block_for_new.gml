graph [
  directed 1
  node [
    id 0
    label "0"
    pos 123
    pos 338
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 195
    pos 340
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 272
    pos 343
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 340
    pos 341
    name "block_,"
    data "block_,"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 420
    pos 335
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 509
    pos 335
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 598
    pos 337
    name "}"
    data "}"
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
    target 3
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
]
