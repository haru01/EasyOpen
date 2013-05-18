# -*- coding: utf-8 -*-
import re
import sublime
import sublime_plugin
from helper import CommandExecutor, current_word, current_word_region


class PasteMethodSnippetCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        self.items = self._items()
        print self.items
        self.window.show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def _items(self):
        # NOTE: お試し版。しばらく触ってみて後で修正するかも
        lines = self.run_cmd(['ag', '--nocolor', 'def\s' + current_word(), '.easyopen_index'])['out'].split("\n")
        return list(set([line.split("def ")[1] for line in lines if line != '']))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        method_def = self.items[picked]
        self.erase_current_word()
        view = sublime.active_window().active_view()
        view.run_command("insert_snippet", {"contents": self.to_snippet_str(method_def)})

    def erase_current_word(self):
        view = sublime.active_window().active_view()
        edit = view.begin_edit()
        view.erase(edit, current_word_region())
        view.end_edit(edit)

    def to_snippet_str(self, str):
        # NOTE: お試し版。 しばらく触ってみて後で修正するかも
        tmp, num = re.subn(r'([^,()]+)', r'${__tmp_number__:\1}', str)
        for i in range(num+1):
            if i == 0:
                tmp = re.sub(r'\${__tmp_number__:([^,()]+)}', r'\1', tmp, 1)
                print tmp
            if i != 0:
                tmp = tmp.replace('${__tmp_number__:', "${%d:" % i, 1)
        return tmp
