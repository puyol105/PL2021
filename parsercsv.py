import csv
import sys
import re

file_name = sys.argv[1]

orig_stdout = sys.stdout
f = open(file_name + '.json', 'w')
sys.stdout = f

with open(file_name + '.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';') # TODO - provavelmente temos de fazer isto com regex
    line_count = 0
    categories = {}
    lists = {}
    print('[')
    for row in csv_reader:
        columns_nr = len(row)
        if line_count == 0:
            i=0
            while i < columns_nr:
                categories[i] = row[i]
                # print(re.search("$*",f'{categories[i]}'))
                #    lists.add(categories[i])
                i+=1
            # TODO - usar regex para ver se alguma categoria tem *
            # TODO - fazer o avg, sum, min e max usando regex para ver se tem isso depois do *
            line_count += 1
        else:
            # while line_nr -1 != line_count:
            i=0
            total = ""
            while i < len(categories):
                if i == len(categories)-1:
                    total += f"\"{categories[i]}\": \"{row[i]}\"    "
                else:
                    total += f"\"{categories[i]}\": \"{row[i]}\",\n    "
                i+=1
            # TODO - tirar a virgula da ultima linha
            print(f'  {{\n    {total} \n  }},')
            line_count += 1
    print(']')


sys.stdout = orig_stdout
f.close()