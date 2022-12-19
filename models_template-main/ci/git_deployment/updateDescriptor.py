# Copy the deployment descriptors in the deployment path to the GitOps controller
import pickle
import os
from jproperties import Properties

descriptorPath = ""
with open('temp/descriptorPath.txt', 'r') as descHandle:
    descriptorPath = descHandle.read()
print("retrieved descriptorPath: " + descriptorPath)

clusterName = os.environ['PROMOTION_CLUSTER']

print(str(descriptorPath))
for root, dirs, files in os.walk(descriptorPath):
    for fileName in files:
        if ".git" in root:
            continue
        filePath = root + "/" + fileName
        print("Moving " + filePath + " to the ModelOpsRepository")
        podDesc = ""
        with open(filePath, 'r') as descHandle:
            podDesc = descHandle.read()

        if (len(podDesc) == 0):
            print("No content found in " + filePath)
            continue
            
        customPath = 'ci/custom/' + clusterName
        
        customProperties = Properties()
        with open(customPath + '/custom_properties.properties', 'rb') as read_prop:
            customProperties.load(read_prop)
            
        propertyList = customProperties.items()

        for item in propertyList:
            print('replacing property: ' + item[0])
            propertyValue = '${' + item[0] +'}' 
            podDesc = podDesc.replace(propertyValue, item[1].data)
            print(podDesc)
        
        print(filePath)
        with open(filePath, 'w') as descHandle:
            descHandle.write(podDesc)
