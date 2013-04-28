# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor


class OpenGemWithBundleCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        self.items = self.items_with_bundle_list()
        self.window.show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_with_bundle_list(self):
        result = self.run_cmd(['bundle', 'list'])
        # TODO: error
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        gem_name = self.items[picked][3:].split(' ')[1]
        self.async_run_cmd_none_callback(['bundle', 'open', gem_name])
