def checking_HTML_correctness(filename):
  """
  Funkcja ma za zadanie sprawdzać poprawność składni dokumentu HTML.
  Jako argument przyjmuje nazwę pliku, który ma sprawdzić.
  Zwraca True jeśli dokument jest poprawny składniowo i False jeśli nie jest.
  """
  file_obj = open(filename, 'r')
  text = file_obj.read()
  if chechbrackets(text):
    return True
  else:
    return False

import sys

special_obj = ["area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr", "!DOCTYPE"]

class Stack():
  def __init__(self):
    self.l = []
  
  def push(self, item):
    self.l.append(item)

  def pop(self):
    return self.l.pop()

  def peek(self):
    return self.l[-1]

  def size(self):
    return len(self.l)
  
  def is_empty(self):
    return self.l == []


def chechbrackets(text):
  st = Stack()
  i = 0
  roof = len(text)

  while i < roof:
    el = text[i]
    if el  == "<":
      i += 1
      while text[i] == " " and i < roof:
        i += 1
      if i >= roof:
        break
      j = i
      while text[i] != " " and text[i] != ">" and i < roof:
        i += 1
      name = text[j : i]
      ###COMMENT###
      if name == "!--":
        if i + 3 < roof:
          while text[i : i + 3] != "-->" and i + 3 < roof:
            i+=1
      else:
        while text[i] != "<" and text[i] != ">" and i < roof:
          i += 1
        if text[i] == "<":
          return False #opening tag in tag
        elif text[i] == ">":
          if name in special_obj:
            continue
          ###CHECKING STACK###
          if name[0] == "/":
            if st.is_empty():
              return False
            if st.pop() != name[1 : ]:
              return False
          else:
            st.push(name)
    else:
      i += 1

  if st.is_empty():
    return True
  return False

def check(filename):
  with open(filename) as code:
    code = code.read()
    if chechbrackets(code):
      print("Correct")
    else:
      print("Incorrect")            

def main(files):
  for i in files:
    check(i)

if __name__ == "__main__":
  main(sys.argv[1:])
