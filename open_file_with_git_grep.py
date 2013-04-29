# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor


class OpenFileWithGitGrepCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Git Grep:', '', self.on_done, None, None)

    def on_done(self, input):
        self.items = self.items_git_grep(input)
        print self.items
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_grep(self, key):
        results = self.run_cmd(['git', 'grep', '-n', key])
        # TODO Error, file name, IF Rename, If Delete
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        picked_file = self.items[picked].split(' ')[0]
        self.window.open_file(picked_file, sublime.ENCODED_POSITION)
