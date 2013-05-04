# -*- coding: utf-8 -*-
import sublime_plugin
import webbrowser
import os
import threading
import sublime
from subprocess import Popen, PIPE


class CommandExecutor:
    def env(self):
        return {'PATH': os.environ['PATH'], 'EDITOR': 'subl'}

    # NOTE: Main thread only
    def root_directory(self):
        try:
            # sublime text 3
            return sublime.active_window().project_data()['folders'][0]['path']
        except:
            # sublime text 2
            return sublime.active_window().folders()[0]

    def file_name_full_path(self, file_name):
        return os.path.join(self.root_directory(), file_name)

    def popen(self, env, cwd, *popen_args):
        return Popen(*popen_args, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)

    def run_cmd(self, *popen_args):
        proc = self.popen(self.env(), self.root_directory(), *popen_args)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {'okay': okay, 'out': stat[0], 'err': stat[1]}

    def async_run_cmd_none_callback(self, *popen_args):
        def __report(result):
            print result
        self.async_run_cmd(__report, *popen_args)

    def async_run_cmd(self, callback=None, *popen_args):
        cwd = self.root_directory()
        env = self.env()

        def run_in_thread(callback, env, cwd, popen_args):
            proc = self.popen(env, cwd, *popen_args)
            proc.wait()
            stat = proc.communicate()
            okay = proc.returncode == 0
            if callback is not None:
                callback({'okay': okay, 'out': stat[0], 'err': stat[1]})
            return

        thread = threading.Thread(target=run_in_thread,
                                  args=(callback, env, cwd, popen_args))
        thread.start()
        return thread


class ProgressBar(object):
    def __init__(self, thread, message, success_message, timeout=30000):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.timeout = timeout
        self.current_time = 0
        sublime.set_timeout(lambda: self.run(), 500)

    def is_timeout(self):
        return self.is_timeout

    def run(self, i="."):
        self.current_time = self.current_time + 500
        if self.timeout < self.current_time:
            sublime.status_message("Stop: %s. Please another keyword" % self.message)
            CommandExecutor().run_cmd(["pkill", "-f", "EasyOpen/ag_in_gems.sh"])
            return
        if not self.thread.is_alive():
            # TODO: fail message
            sublime.status_message(self.success_message)
            return
        sublime.status_message('%s [%s]' % (self.message, ' ' + i))
        sublime.set_timeout(lambda: self.run(i+"."), 500)


class SearchWithBrowserCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Search:', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, input):
        url = self.url_search(input)
        webbrowser.open_new_tab(url)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass
