#!/usr/bin/env python
"""
Zaprojektuj i przeprowadź eksperyment porównujący wydajność implementacji kolejek QueueBaB i QueueBaE.
"""
import L4_ZAD1
import timeit

tests = 100000
queue_a = L4_ZAD1.QueueBaB()
queue_b = L4_ZAD1.QueueBaE()

test1_queueBaB = timeit.Timer("queue_a.enqueue(True)", "from __main__ import queue_a")
test1_queueBaE = timeit.Timer("queue_b.enqueue(True)", "from __main__ import queue_b")

adding_timeBaB =  test1_queueBaB.timeit(number = tests)
adding_timeBaE =  test1_queueBaE.timeit(number = tests)

test2_queueBaB = timeit.Timer("queue_a.dequeue()", "from __main__ import queue_a")
test2_queueBaE = timeit.Timer("queue_b.dequeue()", "from __main__ import queue_b")

removing_timeBaB = test2_queueBaB.timeit(number = tests)
removing_timeBaE = test2_queueBaE.timeit(number = tests)

print("QueueBaB\n" + "-"*10 + "\n" +
"Time for add {} elements to queeuBaB : {} sec\n".format(tests, adding_timeBaB) +
"Time for pop {} elements from queeuBaB : {} sec\n".format(tests, removing_timeBaB) +
"Total time : {} sec\n".format(removing_timeBaB + adding_timeBaB))

print("QueueBaE\n" + "-"*10 + "\n" +
"Time for add {} elements to queeuBaE : {} sec\n".format(tests, adding_timeBaE) +
"Time for pop {} elements from queeuBaE : {} sec\n".format(tests, removing_timeBaE) + 
"Total time: {} sec\n".format(removing_timeBaE +adding_timeBaE))
