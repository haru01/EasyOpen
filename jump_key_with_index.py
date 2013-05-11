# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, IndexLine, env, current_word


# TODO: Error
class JumpKeyWithIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.items = self.items_git_grep(current_word())
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_git_grep(self, key):
        sh = sublime.packages_path() + "/EasyOpen/search_index.sh"
        _key = env()['KEYWORD_DEF'] + '+' + key
        results = self.run_cmd([sh, _key])
        return [item.decode('utf-8') for item in results['out'].split('\n') if item != '']

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)
