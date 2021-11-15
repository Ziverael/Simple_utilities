import timeit

def probability(n, k, p):
  coeff = 1 - p
  p_expr = p / coeff
  prob, count_mult = fast_expon(n, coeff)
  ingred = 1
  binom_val = 1
  exp_val = 1

  for i in range(1, k + 1):
    binom_val *= (n - i + 1) / i
    exp_val *= p_expr
    ingred +=  exp_val * binom_val
    count_mult += 4
  prob *= ingred
  # w ciele funkcji umieść swój kod realizujący cel zadania;
  # argument 'n' niech będzie liczbą prób;
  # argument 'k' niech będzie maksymalną liczbą sukcesów;
  # argument 'p' niech będzie prawdpodobieństwem sukcesu w pojedynczej próbie;
  # w zmiennej 'prob' zwróć oczekiwane prawdopodobieństwo;
  # w zmiennej 'count_mult' zwróć liczbę mnożeń, jaką wykonał Twój program;
  # jeśli potrzebujesz, możesz dopisać również inne funkcje (pomocnicze), 
  # jednak główny cel zadania musi być realizowany w tej funkcji;
  return (prob, count_mult)

def binom(n, k):
  """
  Return binomial (n k) and multiplication number.
  """
  out = n
  for i in range(1, k):
    out *= (n - i)
    out /= (i + 1)
  count_mult = 2 * (k - 1)
  return int(out), count_mult

def prim_expon(exponent, x):
  prod = x
  for i in range(exponent - 1):
    prod *= x
  count_mult = exponent - 1
  return prod, count_mult

def fast_expon(exponent, x):
  """
  Return x ** m in efficient way and multiplication count.
  Code based on Maciej M. Sysło "Algorytmy"
  """
  out = 1
  prod = x
  base = exponent
  count_mult = 0 
  while base > 0:
    if base & 1: #works as modulo
      out *= prod
      count_mult += 1

    base = base // 2
    count_mult += 1

    prod *= prod
    count_mult += 1

  return out, count_mult


def test_expon_func():
  print(fast_expon(500, 2))
  print(prim_expon(500, 2))
  print(fast_expon(200, 3))
  print(fast_expon(200, 3))

  time1 = timeit.Timer("prim_expon(8030, 7)","from __main__ import prim_expon")
  print(time1.timeit(number = 1000))
  time2 = timeit.Timer("fast_expon(8030, 7)","from __main__ import fast_expon")
  print(time1.timeit(number = 1000))
  time3 = timeit.Timer("fast_power(8030, 7)","from __main__ import fast_power")
  print(time1.timeit(number = 1000))


def main():
  #test_expon_func()
  print(probability(8, 5  , 0.3))
  print(probability(4, 2, 0.5))
  print(probability(7, 3, 0.2))

if __name__ == "__main__":
  main()
