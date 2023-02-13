import re, sys
import xml.etree.ElementTree as ET

# fetch type of upgrade code from bash arguments
# 0 is Major
# 1 is Minor
# 2 is Patch
type_of_upgrade = str(sys.argv[1])

# fetch commit message from bash arguments
change_log_update = str(sys.argv[2])


# version_file_name dictates where the version file is located that serves as
# placeholder for all versioning
version_file_name = 'version.txt'

# changelog_file_name dictates where the changelog file is located
changelog_file_name = 'changelog.md'

# changelog_file_name dictates where the changelog file is located
branch_changelog_file_name = 'branch_changelog.md'

# xml_file_name dictates where XML file is located
xml_file_name = './etc/config.xml'

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
    updateRegex = re.compile(updateRegexString)

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
def updateChangelog(version, new_lines, changelog_lines):
    changelog_lines[2] = '## version: ' + version + '\n'
    lines_part1 = changelog_lines[:8]
    lines_part2 = changelog_lines[8:]
    updatedLines = ''

    type_of_upgrade = int(type_of_upgrade)

    if (type_of_upgrade == 0) :
        new_lines = '\n\n**' + version + '**\n' + new_lines
        lines_part1.append(new_lines)
        lines_part1.append('\n')
        lines_part1.append('---')
        lines_part1.append('\n')
    else :
        lines_part1[7] = '\n\n**' + version + '**\n'
        lines_part1.append(new_lines)
        lines_part1.append('\n')

    updatedLines = lines_part1 + lines_part2
    
    return updatedLines

# update_branch_changelog(new_lines) updates the branch changelog changelog with latest commits and some formatting
def update_branch_changelog(new_lines, change_log_update) :
    if not new_lines :
        new_lines = [] 
    lines = []
    lines.append('\n')
    lines.append(change_log_update)
    lines.append('\n')
    return new_lines + lines

# processXML(versiion) takes version input and writes to the config.xml
def processXML(version):
    # read XML file and set root to root variable
    tree = ET.parse(xml_file_name)
    root = tree.getroot()

    # find version tag and set the version to proper version
    for version in root.iter('tag'):
        version.text = version

    # write data back to file
    tree.write('./etc/config.xml')

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

# Execution steps for updating branch specific changelog - Steps below
# 1. if type_of_upgrade is 'branch' we will:
# 2. Read the file and acquire lines from branch_changelog.md
# 3. Append the commit messages into branch changelog

if (type_of_upgrade == 'branch') :
    new_lines = readFile(branch_changelog_file_name)
    new_lines = update_branch_changelog(new_lines, change_log_update)
    writeToFile(new_lines, branch_changelog_file_name)

else :

    # Execution steps for updating version functionality - Steps below
    # 1. Read the file and acquire the lines
    # 2. Determine type of upgrade that needs to be procesed
    # 3. Process the versioning update
    # 4. Write the update to the file
    version_file_lines = readFile(version_file_name)

    type_of_upgrade = int(type_of_upgrade)

    if type_of_upgrade == 0 :
        version_to_write = updateMajorVersion(version_file_lines)
    elif type_of_upgrade == 1 :
        version_to_write = updateMinorVersion(version_file_lines)
    elif type_of_upgrade == 2 :
        version_to_write = updatePatchVersion(version_file_lines)

    writeToFile(version_to_write, version_file_name)

    # Extecution steps for updating changelog functionality - Steps below
    # 1. Read the master changelog file and acquire the lines
    # 2. Read the branch changelog file
    # 3. Update the changelog with the proper formatting
    # 4. Write the update to the changelog file
    # 5. Clear the branch changelog file

    changelog_file_lines = readFile(changelog_file_name)

    branch_changelog_lines = readFile(branch_changelog_file_name)

    updated_changelog_file_lines = updateChangelog(version_to_write, branch_changelog_lines, changelog_file_lines)

    writeToFile(updated_changelog_file_lines, changelog_file_name)

    writeToFile([], branch_changelog_file_name)
