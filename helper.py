# -*- coding: utf-8 -*-
import sublime_plugin
import webbrowser
import os
import threading
import sublime
from subprocess import Popen, PIPE


class CommandExecutor:
    def env(self):
        return {'PATH': os.environ['PATH'], 'EDITOR': 'subl'}

    # NOTE: Main thread only
    def root_directory(self):
        try:
            # sublime text 3
            return sublime.active_window().project_data()['folders'][0]['path']
        except:
            # sublime text 2
            return sublime.active_window().folders()[0]

    def file_name_full_path(self, file_name):
        return os.path.join(self.root_directory(), file_name)

    def popen(self, env, cwd, *popenArgs):
        return Popen(*popenArgs, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)

    def run_cmd(self, *popenArgs):
        proc = self.popen(self.env(), self.root_directory(), *popenArgs)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {'okay': okay, 'out': stat[0], 'err': stat[1]}

    def async_run_cmd_none_callback(self, *popenArgs):
        def __report(result):
            print result
        self.async_run_cmd(__report, *popenArgs)

    def async_run_cmd(self, callback=None, *popenArgs):
        cwd = self.root_directory()
        env = self.env()

        def runInThread(callback, env, cwd, popenArgs):
            proc = self.popen(env, cwd, *popenArgs)
            proc.wait()
            stat = proc.communicate()
            okay = proc.returncode == 0
            if callback is not None:
                callback({'okay': okay, 'out': stat[0], 'err': stat[1]})
            return

        thread = threading.Thread(target=runInThread,
                                  args=(callback, env, cwd, popenArgs))
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
