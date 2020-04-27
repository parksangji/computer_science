datatype pattern = Wildcard | Variable of string | UnitP | ConstP of int | TupleP of pattern list | ConstructorP of string * pattern
datatype valu = Const of int | Unit | Tuple of valu list | Constructor of string * valu

fun check_pat pat =
	let
		fun merge (PAT, StringList) = 
			case PAT of
				Variable string_x => StringList @ [string_x]
				| TupleP pattern_list => (
					case pattern_list of
					[] => StringList
					| p::pattern_list'=>merge(p,StringList) @ merge(TupleP pattern_list',[])
					)
				| ConstructorP(_,p) => merge (p, StringList)
				| _  => StringList

		fun case1 PAT =
			case PAT of
				Variable string_x => [string_x]
				| TupleP pattern_list => List.foldl merge [] pattern_list
				| ConstructorP(_,p) => case1 p
				| _  => []

		fun check (StringList, str1) = List.exists (fn str2 => str1=str2) StringList
		fun case2 StringList =
			case StringList of
				[] => false
				| s::ss => check(ss, s) orelse case2(ss)
	in
		not ((case2 o case1) pat)
	end
		

fun  match (v,p) =
	case p of
		Wildcard => SOME []
		 | Variable s => SOME [(s,v)]
		 | UnitP => (
			case v of 
				Unit => SOME []
				| _ => NONE )
		 | ConstP int_n => (
			case v of
				 Const m => if int_n=m then SOME [] else NONE
				| _ => NONE )
		 | TupleP pattern_list => (
			case v of
				Tuple valu_list => (
					let
						val valu_pattern_list=ListPair.zip(valu_list,pattern_list)
						fun isMatch (valu_pattern_list_help: (valu*pattern) list) = (
							case valu_pattern_list_help of
								[] => true
								| head::tail => isSome( match(#1 head, #2 head) ) andalso isMatch(tail)
						)
						fun  binding (valu_pattern_list_help: (valu*pattern) list) = (
							case valu_pattern_list_help of
								[] => []
								| head::tail => valOf( match(#1 head, #2 head) ) @ binding(tail)
						)
					in
						if isMatch(valu_pattern_list) then SOME(binding valu_pattern_list) else NONE
					end
				)
				| _ => NONE )
		 | ConstructorP (string_1,pattern) => (
			case v of 
				Constructor (string_2, valu) =>
					if (string_1=string_2) andalso isSome(match(valu, pattern))
					then match(valu, pattern)  else NONE
				| _ => NONE )
(* 
    type name = string

    datatype RSP = ROCK
                  | SCISSORS
                  | PAPER
    
    fun onlyOne(one:RSP) = Cons(one, fn() => onlyOne(one))
    fun alterTwo(one:RSP, two:RSP) = Cons(one, fn() => alterTwo(two, one))
    fun alterThree(one:RSP, two:RSP, three:RSP) = Cons(one,fn() => alterThree(two, three, one))
    val r = onlyOne(ROCK)
    val s = onlyOne(SCISSORS)
    val p = onlyOne(PAPER)
    val rp = alterTwo(ROCK, PAPER)
    val sr = alterTwo(SCISSORS, ROCK)
    val ps = alterTwo(PAPER, SCISSORS)
    val srp = alterThree(SCISSORS, ROCK, PAPER)
    fun next(strategyRef) = 
        let val Cons(rsp, func) = !strategyRef in 
            strategyRef := func();
            rsp
        end


    val winner = whosWinner(MATCH(PLAYER("s", ref s), MATCH(PLAYER("rp", ref rp), PLAYER("r", ref r))));LAYER("r", ref r)))); *)