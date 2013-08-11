# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, current_word, LOCATION_CACHE


# TODO: Error
class OpenFileWithIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Index Search:', current_word(), self.on_done, None, None)

    def on_done(self, input):
        self.items = self._items(input)
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def _items(self, key):
        sh = sublime.packages_path() + "/EasyOpen/search_index.sh"
        results = self.run_cmd(["/bin/sh", sh, key.replace(' ', '\s')])
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        LOCATION_CACHE.appendCurrentLocation()
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)
