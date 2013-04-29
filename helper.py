# -*- coding: utf-8 -*-
import sublime_plugin
import webbrowser
import os
import threading
from subprocess import Popen, PIPE


class CommandExecutor:
    def env(self):
        return {'PATH': os.environ['PATH'], 'EDITOR': 'subl'}

    def run_cmd(self, *popenArgs):
        proc = Popen(*popenArgs, env=self.env(), stdout=PIPE, stderr=PIPE)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {'okay': okay, 'out': stat[0], 'err': stat[1]}

    def async_run_cmd_none_callback(self, *popenArgs):
        def __report(result):
            print result
        self.async_run_cmd(__report, *popenArgs)

    def async_run_cmd(self, callback=None, *popenArgs):
        def runInThread(callback, popenArgs):
            # TODO cwd
            proc = Popen(*popenArgs, env=self.env(), stdout=PIPE, stderr=PIPE)
            proc.wait()
            stat = proc.communicate()
            okay = proc.returncode == 0
            if callback is not None:
                callback({'okay': okay, 'out': stat[0], 'err': stat[1]})
            return

        thread = threading.Thread(target=runInThread,
                                  args=(callback, popenArgs))
        thread.start()
        return thread


class SearchWithBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Get the search item
        self.window.show_input_panel('Search:', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, input):
        url = self.url_search(input)
        webbrowser.open_new_tab(url)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass
