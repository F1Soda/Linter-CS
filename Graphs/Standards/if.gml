graph [
  directed 1
  node [
    id 0
    label "0"
    pos 110
    pos 341
    name "if"
    data "if"
    should_check_offset "default"
  ]
  node [
    id 1
    label "1"
    pos 178
    pos 342
    name "_"
    data " "
    should_check_offset "default"
  ]
  node [
    id 2
    label "2"
    pos 220
    pos 342
    name "("
    data "("
    should_check_offset "default"
  ]
  node [
    id 3
    label "3"
    pos 260
    pos 344
    name "expression_)"
    data "expression_)"
    should_check_offset "default"
  ]
  node [
    id 4
    label "4"
    pos 305
    pos 334
    name ")"
    data ")"
    should_check_offset "default"
  ]
  node [
    id 5
    label "5"
    pos 588
    pos 344
    name "block"
    data "block"
    should_check_offset "default"
  ]
  node [
    id 6
    label "6"
    pos 493
    pos 303
    name "line"
    data "line"
    should_check_offset "default"
  ]
  node [
    id 7
    label "7"
    pos 565
    pos 303
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 8
    label "8"
    pos 662
    pos 342
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 9
    label "9"
    pos 681
    pos 408
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 10
    label "10"
    pos 722
    pos 343
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 11
    label "11"
    pos 779
    pos 343
    name "}"
    data "}"
    should_check_offset "default"
  ]
  node [
    id 12
    label "12"
    pos 412
    pos 398
    name "{"
    data "{"
    should_check_offset "default"
  ]
  node [
    id 13
    label "13"
    pos 369
    pos 317
    name "\n"
    data "\n"
    should_check_offset "false"
  ]
  node [
    id 14
    label "14"
    pos 468
    pos 414
    name "increase_offset"
    data "increase_offset"
    should_check_offset "default"
  ]
  node [
    id 15
    label "15"
    pos 544
    pos 406
    name "\n"
    data "\n"
    should_check_offset "default"
  ]
  node [
    id 16
    label "16"
    pos 354
    pos 373
    name "decrease_offset"
    data "decrease_offset"
    should_check_offset "default"
  ]
  node [
    id 17
    label "17"
    pos 412
    pos 297
    name "line_or_block"
    data "line_or_block"
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
    target 4
  ]
  edge [
    source 4
    target 13
  ]
  edge [
    source 5
    target 8
  ]
  edge [
    source 6
    target 7
  ]
  edge [
    source 8
    target 10
  ]
  edge [
    source 9
    target 11
  ]
  edge [
    source 10
    target 11
  ]
  edge [
    source 12
    target 14
  ]
  edge [
    source 13
    target 17
  ]
  edge [
    source 14
    target 15
  ]
  edge [
    source 15
    target 5
  ]
  edge [
    source 15
    target 9
  ]
  edge [
    source 16
    target 12
  ]
]
