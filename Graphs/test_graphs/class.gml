graph [
  directed 1
  node [
    id 0
    label "0"
    pos 82
    pos 266
    name "class"
    data "class"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 145
    pos 264
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 193
    pos 274
    name "identifier"
    data "identifier"
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 278
    pos 278
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 194
    pos 316
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 216
    pos 366
    name "heritage"
    data "heritage"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 87
    pos 316
    name "struct"
    data "struct"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 78
    pos 210
    name "interface"
    data "interface"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 396
    pos 275
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
    target 8
    condition "default"
  ]
  edge [
    source 4
    target 5
    condition "default"
  ]
  edge [
    source 5
    target 3
    condition "default"
  ]
  edge [
    source 6
    target 1
    condition "default"
  ]
  edge [
    source 7
    target 1
    condition "default"
  ]
]
