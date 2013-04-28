# -*- coding: utf-8 -*-
import sublime_plugin
import webbrowser
import os
from subprocess import Popen, PIPE


class RunCmdCommand(sublime_plugin.WindowCommand):
    def exec_cmd(self, cmd, args=[], source='', cwd='', env=None):
        if cwd == '':
            cwd = self.window.folders()[0]  # NOTO:  bug case...
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
