; Function to calculate square of a number
(define (square x)
  (* x x))

; Function to calculate absolute value
(define (absolute x)
  (if (< x 0)
      (- x)
      x))

; Recursive function to calculate factorial of a number
(define (factorial n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))