import pkg_resources
from subprocess import call
 
for dist in [d for d in pkg_resources.working_set]:
    call("pip3 install --upgrade " + dist.project_name, shell=True)
