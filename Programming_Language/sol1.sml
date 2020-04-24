fun merge(x : int list, y : int list) =
    let fun m(xs : int list, ys : int list) =
        if null xs
        then ys
        else if null ys
        then xs
        else 
            if hd(xs) < hd(ys)
            then hd(xs) :: m(tl(xs),ys)
            else hd(ys) :: m(xs,tl(ys))
        fun delete(q,[]) = []
          | delete(q,t::l) = if q = t then delete(q,l) else t :: delete(q,l)
        fun remove_dup [] = []
         | remove_dup ( q:: l )= q :: remove_dup(delete(q,l))
    in remove_dup(m(x,y))
    end
    


fun reverse(xs : int list) = 
    let fun rev(x : int list ,y : int list) =
            if null x
            then y
            else rev(tl(x),hd(x) :: y)
        in
            rev(xs,[])
        end

fun sigma(a : int , b : int , f : int -> int) =
    if a > b then 0
    else f(a) + sigma(a+1,b,f);

fun digits(d : int) =
    let fun dig(dd : int) =
        if dd < 1
        then [] 
        else (dd mod 10 ) :: dig(dd div 10)
    in reverse(dig(d))
    end
fun additivePersistence(n : int) =
    let 
        val nn = digits(n)
        fun dev(nn : int list) =
            if null nn
            then 0
            else hd(nn) + dev(tl(nn))
    in  if null (tl nn)
        then 0
        else 1+ additivePersistence(dev(nn))
    end

fun digitalRoot(n : int) =
    let
        val nn =digits(n)
        fun dev(nn : int list) =
            if null nn
            then 0
            else hd(nn) + dev(tl(nn))
    in  
        if null (tl nn)
        then hd nn
        else digitalRoot(dev(nn))
    end
