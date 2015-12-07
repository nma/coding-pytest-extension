import os
import subprocess
import docker


class Executor(object):

    def execute(self, codefile, test_io, **kwargs):
        # pipe the input and output into the code files to be run inside a docker container
        proc = subprocess.Popen(['python', codefile], stdin=subprocess.PIPE, \
                                                      stdout=subprocess.PIPE, \
                                                      stderr=subprocess.PIPE)
        # retrieve the responses from the docker container
        # then parse them as normal
        proc.stdin.write(bytes(test_io['input'], 'UTF-8'))
        out, err = proc.communicate()
        out = out.decode("UTF-8")

        if out == test_io['output']: 
            status = True
            message = None
        else:
            status = False
            message = "Got Output: " + out + "Expected Output: " + test_io['output']
        return {"success": status, "message": message}


class DockerExecutor(Executor):

    """Executor that uses a docker exec wrapper to execute programs"""
    def __init__(self):
        # instantiate a docker client
        super().__init__()
        docker_host = os.getenv("DOCKER_HOST")
        self.cli = docker.Client(base_url=docker_host)

    def execute(self, codefile, test_io, **kwargs):
        mem_limit = kwargs['mem_limit'] if 'mem_limit' in kwargs else '128m'
        host_config = self.cli.create_host_config(mem_limit=mem_limit)
        container = self.cli.create_container(image='python:3.5', host_config=host_config)
        #container.start()
        exec_id = self.cli.exec_create(container=container, cmd='python ' + codefile)
        out = self.cli.exec_start(exec_id)

        if out == test_io['output']:
            status = True
            message = None
        else:
            status = False
            message = "Got Output: " + out + "Expected Output: " + test_io['output']
        return {"success": status, "message": message}