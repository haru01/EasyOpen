import sublime_plugin
import webbrowser


def url_search(text):
    return 'http://qa.atmarkit.co.jp/q/search?q=' + text.replace(' ', '%20')


class SearchQaAtItFromInputCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Get the search item
        self.window.show_input_panel('Search:', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, input):
        url = url_search(input)
        webbrowser.open_new_tab(url)

    def on_change(self, input):
        pass

    def on_cancel(self):
        pass
