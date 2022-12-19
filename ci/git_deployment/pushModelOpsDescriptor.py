# Copy the deployment descriptors in the deployment path to the GitOps controller
import pickle
import os

descriptorPath = ""
with open('temp/descriptorPath.txt', 'r') as descHandle:
    descriptorPath = descHandle.read()
print("retrieved descriptorPath: " + descriptorPath)

repo = None
with open('temp/gitRepo.pickle', 'rb') as handle:
    repo = pickle.load(handle)
if repo:
    print("retrieved repository object")
else:
    print("could not open repository object")
    exit()

# select the deployment cluster
appLevels = repo.get_contents('apps')
i = 0
clusterName = os.environ['PROMOTION_CLUSTER']
clusterLocated = False
for appLevel in appLevels:
    if (appLevel.name == clusterName):
        print("located the " + clusterName + " cluster for deployment")
        clusterLocated = True
        break;
    i = i + 1
selectedIndex = i
if clusterLocated == False:
    print("The cluster: " + clusterName + ", could not be located")

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

        fileExists = True
        clusterRootPath = "apps/" + clusterName + "/"
        try:
            fileContents = repo.get_contents(clusterRootPath + filePath)
        except Exception:
            fileExists = False

        if fileExists:
            print("Updating descriptor in the Git repository")
            repo.update_file(clusterRootPath + filePath, "updating deployment", podDesc, fileContents.sha)
        else:
            print("Making initial commit to the Git repository")
            repo.create_file(clusterRootPath + filePath, "initial commit", podDesc)
