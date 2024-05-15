graph [
  directed 1
  node [
    id 0
    label "0"
    pos 133
    pos 266
    name "enum"
    data "enum"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 186
    pos 269
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 297
    pos 268
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 244
    pos 270
    name "identifier"
    data "identifier"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 350
    pos 272
    name "just_block"
    data "just_block"
    should_check_offset "default"
  ]
  edge [
    source 0
    target 1
  ]
  edge [
    source 1
    target 3
  ]
  edge [
    source 2
    target 4
  ]
  edge [
    source 3
    target 2
  ]
]
