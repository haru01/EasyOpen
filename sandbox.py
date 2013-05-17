# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, current_word


def current_word_region():
    view = sublime.active_window().active_view()
    region = view.sel()[0]
    if region.begin() == region.end():
        region = view.word(region)

    return region


class SandboxCommand(sublime_plugin.WindowCommand, CommandExecutor):
    def run(self):
        method_def = self.run_cmd(['ag', '--nocolor', 'def\s' + current_word(), '.easyopen_index'])['out'].split("\n")[0].split("def ")[1]
        view = sublime.active_window().active_view()

        edit = view.begin_edit()
        view.erase(edit, current_word_region())
        view.end_edit(edit)

        view.run_command("insert_snippet", {"contents": method_def})

# 行列番号
# 補完の文字列置換 run(self):
