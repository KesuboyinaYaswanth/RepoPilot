import os
import shutil
import stat
from git import Repo



def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)



def clone_repo(repo_url):

    if os.path.exists('repositories/cloned_repo'):
        shutil.rmtree('repositories/cloned_repo', onexc=remove_readonly)

    repo=Repo.clone_from(repo_url, 'repositories/cloned_repo')
    
    return 'repositories/cloned_repo'
    


        

