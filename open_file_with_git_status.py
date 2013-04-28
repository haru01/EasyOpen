# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor


class OpenFileWithGitStatusCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.items = self.items_git_status()
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_status(self):
        result = self.run_cmd(['git', 'status', '--porcelain'])
        # TODO Error, Japanese file name, IF Rename, If Delete
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        picked_file = self.items[picked][3:]

        sublime.active_window().run_command('open_file', {'file': picked_file})
