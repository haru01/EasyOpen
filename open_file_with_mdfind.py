# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor


class OpenFileWithMdfindCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Mdfind:', '', self.on_done, None, None)

    def on_done(self, input):
        self.items = self.items_mdfind(input)
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_mdfind(self, key):
        results = self.run_cmd(['mdfind', key])
        # TODO Error
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        selected_file_name = self.items[picked]
        self.window.open_file(selected_file_name)
