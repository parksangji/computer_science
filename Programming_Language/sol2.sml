datatype expr = NUM of int
                | PLUS of expr * expr
                | MINUS of expr * expr
datatype formula = TRUE
                 | FALSE
                 | NOT of formula
                 | ANDALSO of formula * formula
                 | ORELSE of formula * formula
                 | IMPLY of formula * formula
                 | LESS of expr * expr

fun Expr(NUM(i)) = i
		  	 	|Expr(PLUS(e1,e2)) = (Expr e1) + (Expr e2)
				|Expr(MINUS(e1,e2)) = (Expr e1) - (Expr e2)
fun eval(TRUE) = true
	|eval(FALSE) = false
	|eval(NOT(e1)) = not (eval e1)
	|eval(ANDALSO(e1,e2)) = (eval e1) andalso (eval e2)
	|eval(ORELSE(e1,e2)) = (eval e1) orelse (eval e2)
	|eval(IMPLY(e1,e2)) = (not (eval e1)) orelse (eval e2)
	|eval(LESS(ex1,ex2)) = (Expr ex1) < (Expr ex2)
        
type name = string
datatype metro = STATION of name
	            | AREA of name * metro
	            | CONNECT of metro * metro
fun checkMetro metro1 =
	    let
			fun STRING_CHECK(name1, name_list) =
				let fun aux(name1,name_list,acc) =
				  		case name_list of
						   [] => acc
						   |hd1::tl1 => (name1 = hd1) orelse (STRING_CHECK(name1, tl1))
				in
				  aux(name1,name_list,false)
				end
		    fun check_metro (metro2, name_list) =
			    case metro2 of
				     STATION (name2) => (STRING_CHECK (name2, name_list)) 
				     |AREA (name3, metro3) => ( check_metro(metro3, name3::name_list) )
			         |CONNECT (metro4, metro5) => (check_metro(metro4,name_list)) andalso (check_metro(metro5,name_list))		 
      	in
		    check_metro(metro1,[])
	    end

datatype 'a lazyList = nullList
		    | cons of 'a * (unit -> 'a lazyList)

fun seq (first, last) =
	    if (first <= last)
	        then cons (first, (fn x => seq (first+1, last)) )
	        else nullList

fun infSeq (first) = cons (first, (fn x => infSeq (first+1)) )


fun firstN (lazyListVal, n) = 
	    if ( n > 0)
	        then case lazyListVal of
		           nullList => []
		          | cons (first, f) => first :: firstN (f(), n-1)
	    else []	

	
fun Nth (lazyListVal, n) =
	    if ( n > 1)
	        then case lazyListVal of
		      nullList => NONE
		      | cons (first, f) => Nth (f(), n-1)
	    else case lazyListVal of
		      nullList => NONE
	      	| cons (first, f) => SOME first

fun filterMultiples (lazyListVal, n) =
	    case lazyListVal of
		       nullList => nullList
	      	| cons (first, f) =>
			if ( (first mod n) = 0 )
		      	then case f() of
				   nullList => nullList
			  	| cons (first2, f2) => cons (first2, (fn () => filterMultiples (f2(),n)) )
		  else  cons (first, (fn () => filterMultiples (f(),n)) )

fun sieve (lazyListVal) =
	      case lazyListVal of
		        nullList => nullList
		        | cons (first, f) => cons (first, (fn x => sieve(filterMultiples(f(), first))))

fun primes () = sieve ( infSeq(2) )