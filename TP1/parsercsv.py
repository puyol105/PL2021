import sys
import re
import functools

file_name = sys.argv[1]

orig_stdout = sys.stdout
f = open(file_name + '.json', 'w')
sys.stdout = f
csv_file = open(file_name, 'r')

objects = csv_file.readlines()
objects_len = len(objects)

names = []
names_len = 0

print('[')

for i in range(len(objects)): 
    pattern = ';|\n'
    if i == 0:
        names = re.split(pattern, objects[i])
        names.pop()
        names_len = len(names)
    else:
        result = re.split(pattern, objects[i])
        print("  {")
        for j in range(len(names)):
            name = re.split('[*]', names[j])
            if len(name) == 1:
                print(f"    \"{name[0]}\": \"{result[j]}\"", end = '')
            if len(name) == 2:
                if name[1] == '':
                    print(f"    \"{name[0]}\": [", end='')
                    r = re.sub('[()]','',result[j])
                    print(f"{r}]", end = '')
                else:
                    print(f"    \"{name[0]}_{name[1]}\": ", end='')
                    r = re.sub('[()]','',result[j])
                    strings = re.split(',', r)
                    inteiros = []
                    for inteiro in strings:
                        inteiros.append(int(inteiro))
                    if name[1] == 'sum':
                        reduced = functools.reduce(lambda a,b : a+b, inteiros)
                        print(round(reduced,2),end='')
                    if name[1] == 'avg':
                        reduced = functools.reduce(lambda a,b : a+b, inteiros)
                        print(round(reduced/len(inteiros),2),end='')
                    if name[1] == 'max':
                        reduced = functools.reduce(lambda a,b : a if a>b else b, inteiros)
                        print(round(reduced,2),end='')
                    if name[1] == 'min':
                        reduced = functools.reduce(lambda a,b : a if a<b else b, inteiros)
                        print(round(reduced,2),end='')
            if j != names_len-1:
                print(",")
            else:
                print("")
        print("  }", end = '')
        if i != objects_len-1:
            print(",")
        else:
            print("")
print(']')

csv_file.close()
f.close()
