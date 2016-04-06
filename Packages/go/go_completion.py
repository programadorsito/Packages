import sublime_plugin
import sublime
import utils
GO_MAIN_MODULE="D:/sublime3/Data/go/go.json"

class goCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        lang=utils.get_language()
        if lang != "go":return
        ultimo=utils.get_last_character()
        if ultimo != ".":return
        d=utils.load_json(GO_MAIN_MODULE)
        word=utils.get_word(-1)
        if d.get(word):
            return utils.get_completion_list(d[word])