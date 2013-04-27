# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import exec_cmd


class OpenFileWithGitStatusCommand(sublime_plugin.WindowCommand):
    force_open = False

    def run(self):
        self.items = self.items_git_status()
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_status(self):
        base_dir = self.window.folders()[0]
        result = exec_cmd('git', args=['status', '--porcelain'], cwd=base_dir)
        # TODO Error, Japanese file name, Async, IF Rename, If Delete
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        picked_file = self.items[picked][3:]

        sublime.active_window().run_command('open_file', {'file': picked_file})
