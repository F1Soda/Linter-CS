graph [
  directed 1
  node [
    id 0
    label "0"
    pos 129
    pos 199
    name "namespace"
    data "namespace"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 186
    pos 203
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 242
    pos 204
    name "identifier"
    data "identifier"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 311
    pos 206
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 537
    pos 211
    name "namespace_block"
    data "namespace_block"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 368
    pos 211
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 417
    pos 209
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 640
    pos 210
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 478
    pos 212
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 699
    pos 208
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 10
    label "10"
    pos 753
    pos 206
    name "}"
    data "}"
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
    target 5
  ]
  edge [
    source 4
    target 7
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
    target 4
  ]
  edge [
    source 9
    target 10
  ]
]
