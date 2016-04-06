import sublime_plugin
import sublime
import utils
class RepeticionListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        lang=utils.get_language()
        if lang in ["css"] or utils.get_last_character()!=".":
            return [(x+"\t(R)", x) for x in list(set(utils.get_views_words()))]