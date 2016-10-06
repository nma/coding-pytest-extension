import os
import subprocess
import docker


class Executor(object):

    def execute(self, codefile, test_io, **kwargs):
        # pipe the input and output into the code files
        # to be run inside a docker container
        proc = subprocess.Popen(['python', codefile],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        # retrieve the responses from the process
        # then parse them as normal
        proc.stdin.write(bytes(test_io['input'], 'UTF-8'))
        out, err = proc.communicate()
        out = out.decode("UTF-8")

        if out == test_io['output']:
            status = True
            message = None
        else:
            status = False
            message = "Got Output: " + out + \
                      "Expected Output: " + test_io['output']
        return {"success": status, "message": message}


class DockerExecutor(Executor):

    """Executor that uses a docker exec wrapper to execute programs"""

    def __init__(self):
        # instantiate a docker client
        super().__init__()
        self.cli = docker.Client()

    def execute(self, codefile, test_io, **kwargs):
        self.cli.pull(repository="python", tag="3.5")
        mem_limit = kwargs['mem_limit'] if 'mem_limit' in kwargs else '128m'

        f = open(codefile)
        full_path = os.path.realpath(f.name)
        f.close()
        host_config = self.cli.create_host_config(mem_limit=mem_limit, binds=[
            full_path + ':/tmp/payload'
        ])
        container = self.cli.create_container(image='python:3.5',
                                              host_config=host_config,
                                              volumes="/tmp/payload",
                                              command='python3 /tmp/payload < ' + test_io['input'])

        try:
            self.cli.start(container=container['Id'])

            proc = subprocess.Popen(['docker', 'logs', container['Id']],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)

            out, err = proc.communicate()
            out = out.decode("UTF-8")

            if out == test_io['output']:
                status = True
                message = None
            else:
                status = False
                message = "Got Output: " + out + \
                          "Expected Output: " + test_io['output']
            return {"success": status, "message": message}
        finally:
            self.cli.remove_container(container=container['Id'], v=True)
