# -*- coding: utf-8 -*-
import sublime
from helper import RunCmdCommand


class OpenGemWithBundleCommand(RunCmdCommand):
    force_open = False

    def run(self):
        self.items = self.items_bundle_list()
        sublime.active_window().show_quick_panel(self.items, self.panel_done, sublime.MONOSPACE_FONT)

    def items_bundle_list(self):
        result = self.exec_cmd('bundle', args=['list'])
        # TODO Error
        return filter(lambda n: n != '', result['out'].split('\n'))

    def panel_done(self, picked):
        if 0 > picked < len(self.items):
            return
        gem_name = self.items[picked][3:].split(' ')[1]
        # result = self.exec_cmd('bundle', args=['open', gem_name]) # can't open...
        path = self.exec_cmd('bundle', args=['show', gem_name])['out'].rstrip()
        self.exec_cmd('open', ['-a', 'Sublime Text 2', path])
