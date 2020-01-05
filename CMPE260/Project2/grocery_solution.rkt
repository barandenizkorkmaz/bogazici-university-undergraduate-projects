#lang scheme
;compiling: yes
;complete: yes

(require racket/include)
(include "grocerydb.rkt")

(define (GET-TRANSPORTATION-COST farmName farmList)(if (and (> (length farmList) 0)(not (eq? farmName (car (car farmList)))))
                                       (GET-TRANSPORTATION-COST farmName (cdr farmList))
                                       (if (= 0 (length farmList))
                                           0
                                           (cadr (car farmList)))
                                       ))

(define (TRANSPORTATION-COST farmName)(GET-TRANSPORTATION-COST farmName FARMS))

(define (GET-AVAILABLE-CROPS farmName farmList)(if (and (> (length farmList) 0)(not (eq? farmName (car (car farmList)))))
                                       (GET-AVAILABLE-CROPS farmName (cdr farmList))
                                       (if (= 0 (length farmList))
                                           '()
                                           (caddr (car farmList)))
                                       ))

(define (AVAILABLE-CROPS farmName)(GET-AVAILABLE-CROPS farmName FARMS))

(define (GET-INTERESTED-CROPS customerName customerList)(if (and (> (length customerList) 0)(not (eq? customerName (car (car customerList)))))
                                       (GET-INTERESTED-CROPS customerName (cdr customerList))
                                       (if (= 0 (length customerList))
                                           '()
                                           (caddr (car customerList)))
                                       ))

(define (INTERESTED-CROPS customerName)(GET-INTERESTED-CROPS customerName CUSTOMERS))

(define (GET-CONTRACT-FARMS customerName customerList)(if (and (> (length customerList) 0)(not (eq? customerName (car (car customerList)))))
                                       (GET-CONTRACT-FARMS customerName (cdr customerList))
                                       (if (= 0 (length customerList))
                                           '()
                                           (cadr (car customerList)))
                                       ))

(define (CONTRACT-FARMS customerName)(GET-CONTRACT-FARMS customerName CUSTOMERS))

(define (IS-MEMBER element list)
                                   (if (null? list) #f
                                    (if(equal? element (car list)) #t
                                       (IS-MEMBER element (cdr list))))) 

(define (GET-CONTRACT-WITH-FARM farmName customerList)(if (and (> (length customerList) 0)(IS-MEMBER farmName (cadr(car customerList))))
                                                         (cons(car(car customerList))(GET-CONTRACT-WITH-FARM farmName (cdr customerList)))
                                                         (if (= 0 (length customerList))
                                                             '()
                                                             (GET-CONTRACT-WITH-FARM farmName (cdr customerList)))
                                        ))

(define (CONTRACT-WITH-FARM farmName)(GET-CONTRACT-WITH-FARM farmName CUSTOMERS))

(define (GET-INTERESTED-IN-CROP cropName customerList)(if (and (> (length customerList) 0)(IS-MEMBER cropName (caddr(car customerList))))
                                                         (cons(car(car customerList))(GET-INTERESTED-IN-CROP cropName (cdr customerList)))
                                                         (if (= 0 (length customerList))
                                                             '()
                                                             (GET-INTERESTED-IN-CROP cropName (cdr customerList)))))

(define (INTERESTED-IN-CROP cropName)(GET-INTERESTED-IN-CROP cropName CUSTOMERS))

(define (min x y)(if (null? y)
                     (if (null? x)
                         0
                         x)
                     (if (< x y)
                         x
                         y)))

(define (GET-MIN-SALE-PRICE cropName cropList)(if (and (> (length cropList) 0)(eq? cropName (car (car cropList))))
                                               (min (caddr (car cropList)) (GET-MIN-SALE-PRICE cropName (cdr cropList)))
                                               (if (= 0 (length cropList))
                                                             '()
                                                             (GET-MIN-SALE-PRICE cropName (cdr cropList)))))


(define (listContains? cropName cropList)(if (null? cropList) #f
                                             (if(equal? cropName (car (car cropList)))
                                                #t
                                                (listContains? cropName (cdr cropList)))))

(define (MIN-SALE-PRICE cropName)(if (listContains? cropName CROPS)
                                     (GET-MIN-SALE-PRICE cropName CROPS)
                                     0))




(define (GET-CROPS-BETWEEN minLim maxLim cropList outputList)(if (and (> (length cropList) 0)(and (>= (caddr (car cropList)) minLim) (<= (caddr (car cropList)) maxLim)))
                                            (if (IS-MEMBER (car (car cropList)) outputList)
                                                (GET-CROPS-BETWEEN minLim maxLim (cdr cropList) outputList)
                                                (GET-CROPS-BETWEEN minLim maxLim (cdr cropList) (append outputList (list (car (car cropList))))))
                                            (if (= 0 (length cropList))
                                                             outputList
                                                             (GET-CROPS-BETWEEN minLim maxLim (cdr cropList) outputList))))
  

(define (CROPS-BETWEEN minLim maxLim)(GET-CROPS-BETWEEN minLim maxLim CROPS '()))

(define (getCropExpenditureOfFarm cropName farmName)(getExpenditureCropFarm cropName farmName CROPS))

(define (getExpenditureCropFarm cropName farmName cropList)(if (and (> (length cropList) 0)(eq? cropName (car(car cropList)))(eq? farmName (cadr(car cropList))))
                                                               (caddr(car cropList))
                                                               (getExpenditureCropFarm cropName farmName (cdr cropList))))

(define (GET-BUY-PRICE customerName cropName farmList cropList)(if (and(> (length farmList) 0)(IS-MEMBER cropName (caddr(car farmList)))(IS-MEMBER (car (car farmList)) (CONTRACT-FARMS customerName)))
                                                             (min (+ (TRANSPORTATION-COST (car(car farmList))) (getCropExpenditureOfFarm cropName (car(car farmList)))) (GET-BUY-PRICE customerName cropName (cdr farmList) cropList))
                                                             (if(= (length farmList) 0)
                                                                 '()
                                                                  (GET-BUY-PRICE customerName cropName (cdr farmList) cropList))
                                                               ))

(define (BUY-PRICE customerName cropName)(GET-BUY-PRICE customerName cropName FARMS CROPS))

(define (GET-TOTAL-PRICE customerName cropList)(if(> (length cropList) 0)
                              (+ (BUY-PRICE customerName (car cropList)) (GET-TOTAL-PRICE customerName (cdr cropList)))
                              0))

(define (TOTAL-PRICE customerName)(GET-TOTAL-PRICE customerName (INTERESTED-CROPS customerName)))
