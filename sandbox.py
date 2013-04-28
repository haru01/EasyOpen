from subprocess import Popen, PIPE
import os
import threading


# class CommandExecutor:
#     def __report(self, result):
#         print result

#     def run_cmd_without_callback(self, *popenArgs):
#         self.run_cmd(self.__report, *popenArgs)

#     def run_cmd(self, callback, *popenArgs):
#         def runInThread(callback, popenArgs):
#             env = {'PATH': os.environ['PATH'],
#                    'EDITOR': 'subl'}
#             proc = Popen(*popenArgs, env=env, stdout=PIPE, stderr=PIPE)
#             proc.wait()
#             stat = proc.communicate()
#             okay = proc.returncode == 0
#             callback({'okay': okay, 'out': stat[0], 'err': stat[1]})
#             return

#         thread = threading.Thread(target=runInThread,
#                                   args=(callback, popenArgs))
#         thread.start()
#         return thread

# a = CommandExecutor()
# a.run_cmd_without_callback(['bundle', 'open', 'rspec-core'])
