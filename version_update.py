import re, sys

# fetch type of upgrade code from bash arguments
# 0 is Major
# 1 is Minor
# 2 is Patch
type_of_upgrade = int(sys.argv[1])

# fetch commit message from bash arguments
change_log_update = str(sys.argv[2])


# version_file_name dictates where the version file is located that serves as
# placeholder for all versioning
version_file_name = 'version.txt'

# changelog_file_name dictates where the changelog file is located
changelog_file_name = 'changelog.md'

# updateMajorVersion(Lines) updates the Major version x.0.0
def updateMajorVersion(Lines) :

    updateRegexString = '^[0-9]+'

    updateRegex = re.compile(updateRegexString)

    versionUpdate = ''
    versionStable = ''

    for line in Lines:
        versionUpdate = updateRegex.search(line).group()
                    
    versionUpdate = int(versionUpdate)
    versionUpdate = versionUpdate + 1

    version = str(versionUpdate) + '.0.0'
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

# updateChangelog(version, lines) updates the changelog with latest commits and some proper formatting
def updateChangelog(version, lines):
    versionCommit = version + ' - ' + change_log_update
    updatedLines = ''
    lines[2] = '## version: ' + version + '\n'
    linesPart1 = lines[:8]
    linesPart2 = lines[8:]
    print(type_of_upgrade)
    if (type_of_upgrade == 0) :
        linesPart1.append(versionCommit)
        linesPart1.append('\n')
        linesPart1.append('\n')
        linesPart1.append('---')
        linesPart1.append('\n')
        linesPart1.append('\n')
        updatedLines = linesPart1 + linesPart2
    else :
        linesPart1.append(versionCommit)
        linesPart1.append('\n')
        linesPart1.append('\n')
        updatedLines = linesPart1 + linesPart2
    
    return updatedLines

# writeToFile(version) takes in version from update functions and writes it to the version file
def writeToFile(contents, filename) :
    file1 = open(filename, 'w')
    file1.writelines(contents)
    file1.close()

# readFile() reads file for use on update functions
def readFile(filename) :
    file1 = open(filename, 'r')
    Lines = file1.readlines()
    file1.close()
    return Lines


# Extecution steps for updating version functionality - Steps below
# 1. Read the file and get acquire the lines
# 2. Determine type of upgrade that needs to be procesed
# 3. Process the versioning update
# 4. Write the update to the file

version_file_lines = readFile(version_file_name)

if type_of_upgrade == 0 :
    version_to_write = updateMajorVersion(version_file_lines)
elif type_of_upgrade == 1 :
    version_to_write = updateMinorVersion(version_file_lines)
elif type_of_upgrade == 2 :
    version_to_write = updatePatchVersion(version_file_lines)

writeToFile(version_to_write, version_file_name)

# Extecution steps for updating changelog functionality - Steps below
# 1. Read the file and get acquire the lines
# 2. Update the changelog with the proper formatting
# 4. Write the update to the changelog file

changelog_file_lines = readFile(changelog_file_name)

updated_changelog_file_lines = updateChangelog(version_to_write, changelog_file_lines)

writeToFile(updated_changelog_file_lines, changelog_file_name)
