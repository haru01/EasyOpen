from subprocess import Popen, PIPE
import os

def exec_cmd(cmd, args = [], source='', cwd = '', env = None):
    if not type(args) is list:
        args = [args]
    else:
        if env is None:
            env = {'PATH': os.environ['PATH']}
        if source == '':
            command = [cmd]+args
        else:
            command = [cmd]+args+[source]
        proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
        stat = proc.communicate()
    okay = proc.returncode == 0
    return {'okay': okay, 'out': stat[0], 'err': stat[1]}
