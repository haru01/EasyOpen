# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, current_word, LOCATION_CACHE


# TODO: Error
class OpenFileWithGitGrepCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Git Grep Search:', current_word(), self.on_done, None, None)

    def on_done(self, input):
        self.items = self.items_git_grep(input)
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_grep(self, key):
        results = self.run_cmd(['git', 'grep', '-n', key])
        return [self._name(item) for item in results['out'].split('\n') if item != '']

    def _name(self, item):
        try:
            return item.decode('utf-8')
        except UnicodeDecodeError:
            return ''

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        LOCATION_CACHE.appendCurrentLocation()
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)
