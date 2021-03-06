# -*- coding: utf-8 -*-
import sublime_plugin
import webbrowser
import os
import threading
import sublime
import re
from subprocess import Popen, PIPE


# TODO: 外部ファイル化
def index_def():
    return sublime.load_settings('EasyOpen.sublime-settings').get('indexs')


def extensions_exclude_rb():
    return [k.lower() for k in index_def().iterkeys() if k != 'RB']


def env():
    return {'PATH': os.environ['PATH'],
            'EDITOR': 'subl',
            'HOME': os.environ['HOME'],
            }


def root_directory():
    try:
        # sublime text 3
        return sublime.active_window().project_data()['folders'][0]['path']
    except:
        # sublime text 2
        return sublime.active_window().folders()[0]


def current_word():
    return view().substr(current_word_region())


def current_word_region():
    region = view().sel()[0]
    if region.begin() == region.end():
        region = view().word(region)
    return region


def view():
    return sublime.active_window().active_view()


def current_row_colum():
    view = sublime.active_window().active_view()
    row, col = view.rowcol(view.sel()[0].end())
    return '%d:%d' % (row+1, col+1)


def current_filename_linenumber():
    view = sublime.active_window().active_view()
    return "%s:%s" % (view.file_name(), current_row_colum())


# filename:linenumber:keyword
class IndexLine:
    def __init__(self, line):
        self.line = line

    def selected_file_name(self):
        if re.match(r'^/', self.line):
            return self.filename_linenumber_only()
        return os.path.join(root_directory(), self.filename_linenumber_only())

    def filename_linenumber_only(self):
        return re.sub(r'^([^:]*:\d*):.*', r'\1', self.line)


class CommandExecutor:
    def popen(self, env, cwd, *popen_args):
        return Popen(*popen_args, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)

    def run_cmd(self, *popen_args):
        proc = self.popen(env(), root_directory(), *popen_args)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {'okay': okay, 'out': stat[0], 'err': stat[1]}

    def async_run_cmd_none_callback(self, *popen_args):
        def __report(result):
            print result
        self.async_run_cmd(__report, *popen_args)

    def async_run_cmd(self, callback=None, *popen_args):
        def run_in_thread(callback, env, cwd, popen_args):
            proc = self.popen(env, cwd, *popen_args)
            proc.wait()
            stat = proc.communicate()
            okay = proc.returncode == 0
            if callback is not None:
                callback({'okay': okay, 'out': stat[0], 'err': stat[1]})
            return

        thread = threading.Thread(target=run_in_thread,
                                  args=(callback, env(), root_directory(), popen_args))
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

    def run(self, dots="."):
        self.current_time = self.current_time + 500
        if self.timeout < self.current_time:
            sublime.status_message("Stop: %s. Please another keyword" % self.message)
            # Note: exit(), join(timeout) ではうまく、プロセスが終了しなかったので kill を使った.
            sh = sublime.packages_path() + "/EasyOpen/kill_easyopen.sh"
            CommandExecutor().run_cmd(["/bin/sh", sh])
            return
        if not self.thread.is_alive():
            # TODO: fail message
            sublime.status_message(self.success_message)
            return
        sublime.status_message('%s [%s]' % (self.message, ' ' + dots))
        sublime.set_timeout(lambda: self.run(dots+"."), 500)


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

class LocationCache(object):
    def __init__(self):
        self.locations = []

    def appendCurrentLocation(self):
        print "append" + current_filename_linenumber()
        self.locations.append(current_filename_linenumber())


    def pop(self):
        return self.locations.pop()


LOCATION_CACHE = LocationCache()
