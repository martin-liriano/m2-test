import re

file1 = open('version.txt', 'r')
Lines = file1.readlines()

stableRegex = re.compile('[0-9]+\.[0-9]+\.')
updateRegex = re.compile('[0-9]+$')

versionUpdate = ''
versionStable = ''
  
for line in Lines:
    print(line)
    versionUpdate = updateRegex.search(line).group()
    versionStable = stableRegex.search(line).group()
                    
versionUpdate = int(versionUpdate)
versionUpdate = versionUpdate + 1

version = versionStable + str(versionUpdate)

file2 = open('version.txt', 'w')

file2.write(version)

file2.close()
