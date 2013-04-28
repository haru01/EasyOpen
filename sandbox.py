import sublime_plugin
import sublime


class SandboxCommand(sublime_plugin.WindowCommand):
    def run(self):
        v = sublime.active_window().new_file()
        v.set_scratch(True)
        v.set_name('sample')
        edit = v.begin_edit()
        v.erase(edit, sublime.Region(0, v.size()))
        v.insert(edit, v.size(), 'before')
        v.end_edit(edit)

        r = sublime.Region(0, 5)
        ## Region : match_dicts
        v.add_regions("inserted", [r], "markup.inserted.diff", "dot", sublime.HIDDEN)
        v.settings().set('command_mode', True)
