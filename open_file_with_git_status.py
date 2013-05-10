# -*- coding: utf-8 -*-
import os
import sublime
import sublime_plugin
from helper import CommandExecutor, root_directory


class GitStausLine:
    def __init__(self, line):
        self.line = line

    def selected_file_name(self):
        picked_file = self.line[3:]
        if " -> " in picked_file:
            picked_file = picked_file.split(' -> ')[1]
        return self.file_name_full_path(picked_file)

    def file_name_full_path(self, file_name):
        return os.path.join(root_directory(), file_name)


# TODO: Error
class OpenFileWithGitStatusCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.items = self.items_git_status()
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_status(self):
        result = self.run_cmd(['git', 'status', '--porcelain'])
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        sublime.active_window().open_file(GitStausLine(self.items[picked]).selected_file_name())

