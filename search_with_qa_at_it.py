from helper import SearchWithBrowserCommand


class SearchWithQaAtItCommand(SearchWithBrowserCommand):
    def url_search(self, text):
        return 'http://qa.atmarkit.co.jp/q/search?q=' + text.replace(' ', '%20')
