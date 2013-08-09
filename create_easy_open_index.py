# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
from helper import CommandExecutor, ProgressBar, index_def, extensions_exclude_rb


# TODO: error
class CreateEasyOpenIndexCommand(sublime_plugin.WindowCommand, CommandExecutor):
    force_open = False

    def run(self):
        rb_create_sh = sublime.packages_path() + "/EasyOpen/rb_create_index.sh"
        create_sh = sublime.packages_path() + "/EasyOpen/create_index.sh"
        del_sh = sublime.packages_path() + "/EasyOpen/delete_index.sh"
        self.run_cmd(["/bin/sh", del_sh])
        # 処理が重たくない前提
        for ext in extensions_exclude_rb():
            print self.run_cmd(["/bin/sh", create_sh, ext, index_def()[ext.upper()].replace('$keyword', '')])

        # ruby は Gemfile先もインデックス用意で処理が重たい前提
        thread = self.async_run_cmd(self.cmd_done, ["/bin/sh", rb_create_sh, index_def()['RB'].replace('$keyword', '')])
        ProgressBar(thread, 'creating index', 'done:!')

    def cmd_done(self, results):
        print results
