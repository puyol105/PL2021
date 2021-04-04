#!/usr/bin/python3

import sys
import re
import functools

file_name = sys.argv[1]

file = open(file_name + '.csv', 'r')
out = open(file_name + '.json', 'w')
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
lines[len(lines)-1] = lines[len(lines)-1] + "\n"

print('[')
for index, line in enumerate(lines):
    print('  {')
    values = re.split(pattern, line)
    for i in range(len(values)-1):
      if result := re.match(r'(\w+)(\*)(sum|avg|max|min)', rows[i]):
        field = gen_reduce(values[i], result.group(3))
        print(f"    \"{result.group(1)}_{result.group(3)}\": {field} ", end='')
      elif result := re.match(r'(\w+)(\*)$', rows[i]):
        field = re.sub(r'[()]','', values[i])
        r = re.sub('[*]','',rows[i])
        print(f"    \"{r}\": [{field}]", end='')
      else:
        print(f"    \"{rows[i]}\": \"{values[i]}\"", end='')
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
