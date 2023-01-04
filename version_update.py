import re, sys

# fetch type of upgrade code from bash arguments
# 0 is Major
# 1 is Minor
# 2 is Patch
typeOfUpgrade = int(sys.argv[1])

# filename dictates where the version file is located that serves as
# placeholder for all versioning
filename = 'version.txt'

# updateMajorVersion(Lines) updates the Major version x.0.0
def updateMajorVersion(Lines) :

    stableRegexString = '\.[0-9]+\.[0-9]+$'
    updateRegexString = '^[0-9]+'

    stableRegex = re.compile(stableRegexString)
    updateRegex = re.compile(updateRegexString)

    versionUpdate = ''
    versionStable = ''

    for line in Lines:
        versionUpdate = updateRegex.search(line).group()
        versionStable = stableRegex.search(line).group()
                    
    versionUpdate = int(versionUpdate)
    versionUpdate = versionUpdate + 1

    version = str(versionUpdate) + versionStable
    return version

# updateMinorVersion(Lines) updates the minor version 0.x.0
def updateMinorVersion(Lines) :

    majorVersionString = ''
    minorVersionString = ''
    patchVersionString = ''

    section = 0

    for line in Lines:
        for c in line:
            if c == '.' :
                section = section + 1
                continue
            if section == 0 :
                majorVersionString = majorVersionString + c
            elif section == 1 :
                minorVersionString = minorVersionString + c
            elif section == 2 :
                patchVersionString = patchVersionString + c
    
    minorVersionString = int(minorVersionString)
    minorVersionString = minorVersionString + 1

    version = majorVersionString + '.' + str(minorVersionString) + '.' + patchVersionString
    return version

# updatePatchVersion(Lines) updates the Patch version 0.0.x
def updatePatchVersion(Lines) :

    stableRegexString = '[0-9]+\.[0-9]+\.'
    updateRegexString = '[0-9]+$'

    stableRegex = re.compile(stableRegexString)
    print('stableRegex', stableRegex)
    updateRegex = re.compile(updateRegexString)
    print('updateRegex', updateRegex)

    versionUpdate = ''
    versionStable = ''

    for line in Lines:
        versionUpdate = updateRegex.search(line).group()
        versionStable = stableRegex.search(line).group()
                    
    versionUpdate = int(versionUpdate)
    versionUpdate = versionUpdate + 1

    version = versionStable + str(versionUpdate)
    return version

# writeToFile(version) takes in version from update functions and writes it to the version file
def writeToFile(version) :

    file2 = open('version.txt', 'w')

    file2.write(version)

    file2.close()

# readFile() reads file for use on update functions
def readFile() :
    file1 = open('version.txt', 'r')
    Lines = file1.readlines()
    return Lines


# Extecution steps for above functionality - Steps below
# 1. Read the file and get acquire the lines
# 2. Determine type of upgrade that needs to be procesed
# 3. Process the versioning update
# 4. Write the update to the file

linesToRead = readFile()

if typeOfUpgrade == 0 :
    versionToWrite = updateMajorVersion(linesToRead)
elif typeOfUpgrade == 1 :
    versionToWrite = updateMinorVersion(linesToRead)
elif typeOfUpgrade == 2 :
    versionToWrite = updatePatchVersion(linesToRead)

writeToFile(versionToWrite)
