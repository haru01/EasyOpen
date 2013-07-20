# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, ProgressBar, env


# TODO: error
class CreateEasyOpenIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        sh = sublime.packages_path() + "/EasyOpen/create_index.sh"
        thread = self.async_run_cmd(self.cmd_done, ["/bin/sh", sh, 'rb', env()['RB_KEYWORD_DEF']])
        ProgressBar(thread, 'creating index', 'done:!')

    def cmd_done(self, results):
        print results
