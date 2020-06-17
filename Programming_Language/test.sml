 fun length xs =
 case xs of
  [] => 0
 | x::xs' => 1 + (length xs')
