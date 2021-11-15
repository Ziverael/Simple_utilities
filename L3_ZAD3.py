import sys

def counting_chars_without_ifs_first_version(filename):
  """
  Return dict of characters and number of repetition in given text.
  """
  file_ref = open(filename, 'r')
  text = file_ref.read()
  text = text.upper()
  text = list(text)
  text.sort()

  char_count = {i : 0 for i in set(text)}
  i = 1
  j = 0
  char_count[text[0]] += 1 #* int(text[i] != text[0])
  roof = len(text)
  while i < roof - 1:
    while ord(text[i]) == ord(text[i - 1]) and i < roof - 1:
      char_count[text[i]] += 1
      i += 1
    
    char_count[text[i]] += 1
    i += 1
  char_count[text[-1]] += 1 * int(text[-1] != text[-2])
  # uzupełnij ciało tej funkcji kodem realizującym cel zadania;
  # w zmiennej 'char_count' zwróć słownik zawierający wszystkie znaki tekstu 
  # jako klucze i ich liczebnoć jako wartości np. {'a': 6, 'b': 2 ...};
  # jeli potrzebujesz, możesz dopisać również inne funkcje (pomocnicze), 
  # jednak główny cel zadania musi być realizowany w tej funkcji;
  return char_count

def counting_chars_without_ifs(filename):
  """
  Return dict of characters and number of repetition in given text.
  The function is boosted version of the previous one.
  """
  file_ref = open(filename, 'r')
  text = file_ref.read()
  text = text.upper()
  counts = {i : 0 for i in set(text)}
  roof = len(text)
  i = 0
  while i < roof:
    counts[text[i]] += 1
    i += 1
  return counts

def main():
  """
  Print dictionary given by counting_chars_without_ifs for filename given in program call 
  """
  u = counting_chars_without_ifs_first_version(sys.argv[1])
  v = counting_chars_without_ifs(sys.argv[1])
  for key in v:
    print(key," => " , u[key], v [key])
  print( u == v)
if __name__ == "__main__":
  main()