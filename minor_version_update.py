import re

# Using readlines()
file1 = open('index.php', 'r')
Lines = file1.readlines()

p = re.compile('[0-9]+\.[0-9]+\.[0-9]+)
  
for line in Lines:
  if 'PREFIX_SOFTWARE_VERSION' in line:
    result = p.search(line)
    countPeriod = 2
    appendedString = ''
    for c in result:
      if c is '.':
        countPeriod = countPeriod - 1
      if countPeriod == 0:
        appendedString += c
               
     appendedString = int(appendedString)
     appendedString = appendedString + 1
