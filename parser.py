#!/usr/bin/python3

import sys
import re
import functools

file = open('teste.csv', 'r')
out = open('out.json', 'w')
sys.stdout = out

def gen_reduce(listaStr, value):
  lista = re.sub('[()]', '', listaStr).split(',')
  inteiros=[]
  reduced=0.0
  for inteiro in lista:
      inteiros.append(int(inteiro))
  if value == 'sum':
      reduced = functools.reduce(lambda a,b : a+b, inteiros)
  if value == 'avg':
      reduced = functools.reduce(lambda a,b : a+b, inteiros)
      reduced = round(reduced/len(inteiros),2)
  if value == 'max':
      reduced = functools.reduce(lambda a,b : a if a>b else b, inteiros)
  if value == 'min':
      reduced = functools.reduce(lambda a,b : a if a<b else b, inteiros)
  return reduced


pattern = ';|\n'
rows = re.split(pattern, file.readline())
lines = file.readlines()

print('[')
for index, line in enumerate(lines):
    print('  {')  #print('index: ', str(index), 'line: ', line)
    values = re.split(pattern, line)
    for i in range(len(values)-1):
      result = re.match(r'(\w+)(\*)?(sum|avg|max|min){0,1}', rows[i])
      if result.group(3):
        field = gen_reduce(values[i], result.group(3))
        print(f"    \"{result.group(1)}_{result.group(3)}\" : {field} ", end='')
      elif result.group(2):
        field = re.sub(r'[()]','', values[i])
        print(f"    \"{rows[i]}\" : [{field}]", end='')
      elif result.group(1):
        print(f"    \"{rows[i]}\" : \"{values[i]}\"", end='')
      if(i<(len(values)-2)):
        print(',')
      else:
        print('\t')

    print('  }', end= '')
    if index<=len(lines)-2:
      print(',')
    else:
      print('\t')
print(']')

file.close()
out.close()
