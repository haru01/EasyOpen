# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, index_def, current_word


easy_open_opened_histories = []


def current_row_colum():
    view = sublime.active_window().active_view()
    row, col = view.rowcol(view.sel()[0].end())
    return '%d:%d' % (row+1, col+1)


def current_filename_linenumber():
    view = sublime.active_window().active_view()
    return "%s:%s" % (view.file_name(), current_row_colum())


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
        easy_open_opened_histories.append(current_filename_linenumber())
        print easy_open_opened_histories
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)


class JumpBackCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        sublime.active_window().open_file(easy_open_opened_histories.pop(), sublime.ENCODED_POSITION)
