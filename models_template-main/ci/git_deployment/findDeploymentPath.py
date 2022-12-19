# look at the results of the last git push and get the contents of the deployment directories that were updated
descriptorPath = None
descriptorPathObj = None
with open('temp/gitReport.txt', 'r') as reportHandle:
    reportLines = reportHandle.readlines()
    for reportLine in reportLines:
        fileItems = reportLine.split("/")
        if (fileItems[1] == 'deployment'):
            descriptorPath = fileItems[0] + "/" + fileItems[1]
            print("Found descriptor path: " + descriptorPath)
            descriptorPathObj = {}
            descriptorPathObj['descriptorPath'] = descriptorPath
            break
if descriptorPath:
    print("writng descpriptorPath to file")
    with open('temp/descriptorPath.txt', 'w') as descriptorHandle:
        descriptorHandle.write(descriptorPath)
