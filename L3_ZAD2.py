import matplotlib.pyplot as plt
import timeit


def ordinary_polynomial_value_calc(coeff, arg):
  value = 0
  count_add = 0
  count_mult = 1
  for i in range(len(coeff)):
    value += coeff[i] * arg ** i
    count_mult += i
  count_add += len(coeff)
  # w ciele tej funkcji zawrzyj kod wyliczający wartość wielomianu w tradycyjny sposób;
  # argument 'coeff' niech będzie listą współczynników wielomianu w kolejności od stopnia zerowego (wyrazu wolego) wzwyż;
  # argument 'arg' niech będzie punktem, w którym chcemy policzyć wartość wielomianu;
  # w zmiennej 'count_mult' zwróć liczbę mnożeń, jakie zostału wykonane do uzyskania tego wyniku;
  # w zmiennej 'count_add' zwróć liczbę dodawań, jakie zostału wykonane do uzyskania tego wyniku;
  return value, count_mult, count_add
  
def smart_polynomial_value_calc(coeff, arg):
  value = coeff[-1]
  count_mult = len(coeff) - 1
  count_add = count_mult
  for i in range(2, len(coeff) + 1):
    value = value * arg + coeff[-i]
  # w ciele tej funkcji zawrzyj kod wyliczający wartość wielomianu w sposób maksymalnie ograniczający liczbę wykonywanych mnożeń;
  # argument 'coeff' niech będzie listą współczynników wielomianu w kolejności od stopnia zerowego (wyrazu wolego) wzwyż;
  # argument 'arg' niech będzie punktem, w którym chcemy policzyć wartość wielomianu;
  # w zmiennej 'count_mult' zwróć liczbę mnożeń, jakie zostału wykonane do uzyskania tego wyniku;
  # w zmiennej 'count_add' zwróć liczbę dodawań, jakie zostału wykonane do uzyskania tego wyniku;
  return value, count_mult, count_add
  
  
# jeśli potrzebujesz, możesz dopisać również inne funkcje (pomocnicze), 
# jednak główne cele zadania muszą być realizowane w powyższych dwóch funkcjach;

def plots():
  data, mult, add = [] ,[[], []], [[], []]
  for i in range(1, 101):
    data.append([])
    for j in range(1, i + 1):
      data[i - 1].append(j)
  for i in data:
    _, buff11, buff12 = smart_polynomial_value_calc(i,1)
    _, buff21, buff22 = ordinary_polynomial_value_calc(i,1)
    mult[0].append(buff11)
    mult[1].append(buff21)
    add[0].append(buff12)
    add[1].append(buff22)
  t = [i for i in range(1, 101)]
  plt.plot(t,mult[0], label = "smart")
  plt.plot(t,mult[1], label = "ordinary")
  plt.xlim(1,40)
  plt.ylim(0,800)
  plt.legend()
  plt.show()

def main():
  print(ordinary_polynomial_value_calc([3,2.5,8,2], 3))
  print(smart_polynomial_value_calc([3, 2.5, 8, 2], 3))

  timer1 = timeit.Timer("ordinary_polynomial_value_calc([3,2.5,8,2], 3)", "from __main__ import ordinary_polynomial_value_calc")
  timer2 = timeit.Timer("smart_polynomial_value_calc([3,2.5,8,2], 3)", "from __main__ import smart_polynomial_value_calc")
  print(timer1.timeit(number = 100))
  print(timer2.timeit(number = 100))
  plots()

if __name__ == "__main__":
  main()