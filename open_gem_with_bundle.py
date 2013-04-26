# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import exec_cmd


class OpenGemWithBundleCommand(sublime_plugin.WindowCommand):
    force_open = False

    def run(self):
        self.items = self.items_bundle_list()
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_bundle_list(self):
        base_dir = self.window.folders()[0]
        result = exec_cmd('bundle', args=['list'], cwd=base_dir)
        # TODO Error
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        gem_name = self.items[picked][3:].split(' ')[1]
        base_dir = self.window.folders()[0]
        # result = exec_cmd('bundle', args=['open', gem_name], cwd=base_dir) # can't open...
        path = exec_cmd('bundle', args=['show', gem_name], cwd=base_dir)['out'].rstrip()
        exec_cmd('open', ['-a', 'Sublime Text 2', path],  cwd=base_dir)
