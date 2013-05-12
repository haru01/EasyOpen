# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, env


easy_open_opened_histories = []


def current_row_colum():
        view = sublime.active_window().active_view()
        row, col = view.rowcol(view.sel()[0].end())
        return '%d:%d' % (row+1, col)


def current_filename_linenumber():
        view = sublime.active_window().active_view()
        return "%s:%s" % (view.file_name(), current_row_colum())


def current_word():
    view = sublime.active_window().active_view()
    region = view.sel()[0]
    if region.begin() == region.end():
        region = view.word(region)
    return view.substr(region)


class JumpKeyWithIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        self.items = self.search_items(current_word())
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def search_items(self, key):
        if len(key) <= 1:
            return []
        sh = sublime.packages_path() + "/EasyOpen/search_index.sh"
        # TODO: 検索条件を見直す
        _key = env()['KEYWORD_DEF'] + '+(self.){0,1}(:){0,1}([\w:]+){0,1}' + key
        # TODO: asyncのほうがよいか
        results = self.run_cmd([sh, _key])
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        easy_open_opened_histories.append(current_filename_linenumber())
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)


class JumpBackCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        sublime.active_window().open_file(easy_open_opened_histories.pop(), sublime.ENCODED_POSITION)
