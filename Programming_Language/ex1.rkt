#lang racket

(define x 3)
(define y (+ x 2))
(define z 5)
(define (silly-triple x)
  (letrec ([y (+ x 2)][f (lambda(z) (+ z y w x))][w (+ x 7)]) (f -9)))
;y = 5 , w = 10 , z = -9
(define (my-if x y z)
  (if x (y) (z)))
(define (fact n)
  (my-if (= n 0)
         (lambda() 1)
         (lambda() (* n (fact (- n 1))))))

(define (my-delay th)
  (mcons #f th))
(define (my-force p)
  (if (mcar p)
      (mcdr p)
      (begin (set-mcar! p #t)
             (set-mcdr! p ((mcdr p)))
             (mcdr p))))

(define (pow x y)
             (if (= y 0)
                 1
                 (* x (pow x (- y 1)))))


(define (number-until stream tester)
  (letrec ([f (lambda (stream ans)
                (let ([pr (stream)])
                  (if (tester (car pr))
                      ans
                      (f (cdr pr) (+ ans 1)))))])
    (f stream 1)))

(define ones (lambda () (cons 1 ones)))
(define nats
  (letrec ([f (lambda (x)
                (cons x (lambda () (f (+ x 1)))))])
    (lambda () (f 1))))
(define powers-of-two
  (letrec ([f (lambda (x)
                (cons x (lambda () (f (* x 2)))))])
    (lambda () (f 2))))



(define (fib2 x)
  (letrec ([f (lambda (acc1 acc2 y)
                (if (= y x)
                    (+ acc1 acc2)
                    (f (+ acc1 acc2) acc1 (+ y 1))))])
    (if (or (= x 1) (= x 2))
        1
        (f 1 1 3))))
(define (fib3 x)
  (letrec ([memo null] ;memo=(4 . 3) (3 . 2) (1 . 1) (2 . 1))
           [f (lambda (x)
                (let ([ans (assoc x memo)])
                  (if ans (cdr ans)
                      (let ([new-ans (if (or (= x 1) (= x 2))
                                         1
                                         (+ (f (- x 1)) (f (- x 1))))])
                        (begin
                          (set! memo (cons (cons x new-ans) memo))
                          new-ans)))))])
    (f x)))