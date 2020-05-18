#lang racket
(provide (all-defined-out))

(define (node_value node) (car node))
(define (node_left_child node) (cadr node))
(define (node_right_child node) (caddr node))

(define (check_bst ROOT)
  (if (null? ROOT) #t
      (letrec ([value (node_value ROOT)]
            [check_right_child_value (lambda(node)
                      (if (null? node) #t
                          (< value (node_value node))))]
            [check_left_child_value (lambda(node)
                      (if (null? node) #t
                          (> value (node_value node))))])
      (and (check_right_child_value (node_right_child ROOT)) (check_left_child_value(node_left_child ROOT)) (check_bst (node_right_child ROOT)) (check_bst (node_left_child  ROOT))))))


(define (apply func ROOT)
  (if (null? ROOT) null
      (list (func (node_value ROOT)) (apply func (node_left_child ROOT)) (apply func (node_right_child ROOT)))))


(define (equals root_value_first root_value_second)
  (letrec ([value_exist (lambda(value ROOT)
                   (if (null? ROOT)  #f
                   (or (= value (node_value ROOT)) (value_exist value (node_left_child ROOT)) (value_exist value (node_right_child ROOT)))))]
           [compare (lambda(ROOT_value_same ROOT_tree)
                 (if (null? ROOT_value_same)  #t
                 (and (value_exist (node_value ROOT_value_same) ROOT_tree) (compare (node_left_child ROOT_value_same) ROOT_tree) (compare (node_right_child ROOT_value_same) ROOT_tree))))])
    (and (compare root_value_first root_value_second) (compare root_value_second root_value_first))))
