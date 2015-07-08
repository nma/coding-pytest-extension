from fabric.api import task
from fabric.operations import local

@task
def test():
    local('python -m unittest discover')

@task
def test_single(name):
    local('python -m unittest test.{}'.format(name))
