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
    pos 316
    pos 261
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 326
    pos 162
    name ";"
    data ";"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 382
    pos 265
    name "just_block"
    data "just_block"
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
    source 2
    target 4
    condition "default"
  ]
  edge [
    source 3
    target 5
    condition "default"
  ]
]
