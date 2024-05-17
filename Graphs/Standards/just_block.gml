graph [
  directed 1
  node [
    id 0
    label "0"
    pos 154
    pos 339
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 312
    pos 346
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 221
    pos 342
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 413
    pos 351
    name "block"
    data "block"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 503
    pos 346
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 598
    pos 351
    name "}"
    data "}"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 2
    condition "default"
  ]
  edge [
    source 1
    target 3
    condition "default"
  ]
  edge [
    source 2
    target 1
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
]
