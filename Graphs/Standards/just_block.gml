graph [
  directed 1
  node [
    id 0
    label "0"
    pos 128
    pos 346
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 343
    pos 351
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 234
    pos 348
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 453
    pos 352
    name "block"
    data "block"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 544
    pos 357
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 635
    pos 357
    name "}"
    data "}"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 2
  ]
  edge [
    source 1
    target 3
  ]
  edge [
    source 2
    target 1
  ]
  edge [
    source 3
    target 4
  ]
  edge [
    source 4
    target 5
  ]
]
