# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, ProgressBar, IndexLine, current_word


# TODO: Error
class OpenFileInGemsCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.window.show_input_panel('Find in Gems', current_word(), self.on_done, None, None)

    def on_done(self, input):
        self.items_in_gems_with_ag(input)

    def items_in_gems_with_ag(self, key):
        ag_sh = sublime.packages_path() + "/EasyOpen/ag_in_gems.sh"
        thread = self.async_run_cmd(self.cmd_done, ["/bin/sh", ag_sh, key.replace(' ', '\s')])
        ProgressBar(thread, 'finding: %s' % key, 'done: %s' % key)

    def cmd_done(self, results):
        self.items = [item for item in results['out'].decode('utf-8').split('\n') if item != '']
        # main スレッド
        sublime.set_timeout(self.panel_open, 0)

    def panel_open(self):
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        sublime.active_window().open_file(IndexLine(self.items[picked]).selected_file_name(), sublime.ENCODED_POSITION)
