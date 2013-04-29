# -*- coding: utf-8 -*-
from helper import SearchWithBrowserCommand


class SearchWithQaAtItCommand(SearchWithBrowserCommand):
    def url_search(self, text):
        return 'http://qa.atmarkit.co.jp/q/search?q=' + text.replace(' ', '%20')


class SearchWithGithubCommand(SearchWithBrowserCommand):
    def url_search(self, text):
        return 'https://github.com/search?q=' + text.replace(' ', '%20')


class SearchWithQiitaCommand(SearchWithBrowserCommand):
    def url_search(self, text):
        return 'http://qiita.com/search?q=' + text.replace(' ', '%20')


class SearchWithStackoverflowCommand(SearchWithBrowserCommand):
    def url_search(self, text):
        return 'http://stackoverflow.com/search?q=' + text.replace(' ', '%20')
