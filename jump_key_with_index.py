# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, index_def, current_word, LOCATION_CACHE


def current_file_extension():
    view = sublime.active_window().active_view()
    return view.file_name().split(".")[-1]


class JumpKeyWithIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        self.items = self._items(current_word())
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def _items(self, key):
        ext = current_file_extension()
        if len(key) <= 1:
            return []
        sh = sublime.packages_path() + "/EasyOpen/search_index.sh"
        _key = index_def()[ext.upper()].replace('$keyword', key)
        print _key
        results = self.run_cmd(["/bin/sh", sh, _key, ext])
        return [item for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        LOCATION_CACHE.appendCurrentLocation()
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)


class JumpBackCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        sublime.active_window().open_file(LOCATION_CACHE.pop(), sublime.ENCODED_POSITION)
