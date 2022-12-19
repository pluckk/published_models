# login to github and get the orchestration repository

import os
import base64
import github
import pickle

accessKey = os.environ['GIT_REPO_CREDS_PSW']
orchestrationRepo = os.environ['GIT_REPOSITORY']

g = github.Github(accessKey)
repo = g.get_user().get_repo(orchestrationRepo)

with open('temp/gitRepo.pickle', 'wb') as handle:
    pickle.dump(repo, handle, protocol=pickle.HIGHEST_PROTOCOL)
