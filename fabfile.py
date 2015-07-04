from fabric.api import task
from fabric.operations import local

@task
def test():
    local('python -m unittest discover')

