import subprocess


class Executor(object):

    def execute(self, codefile, test_io):
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
            if err:
                err = err.decode("UTF-8")
                #import re
                #err = re.escape(err)
            else:
                err = 'None'
            message = "Got Output: " + out + "Expected Output: " + test_io['output']  + " Errors: " + err
        return {"success": status, "message": message}

class SandboxedExecutor(Executor):
    pass
