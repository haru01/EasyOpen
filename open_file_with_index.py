# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, root_directory


# TODO: Error
class OpenFileWithIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Index Search:', '', self.on_done, None, None)

    def on_done(self, input):
        self.items = self.items_git_grep(input)
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_grep(self, key):
        sh = sublime.packages_path() + "/EasyOpen/search_index.sh"
        results = self.run_cmd([sh, key.replace(' ', '\s')])
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)
