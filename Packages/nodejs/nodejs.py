import sublime
import utils
import sublime_plugin

class NodejsListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if utils.get_language()!="nodejs":return
        if utils.is_point():
            modulo=utils.get_back_word()
            core=utils.load_json_packages_path("nodejs", "core.json")
            if core.get(modulo):
                return utils.get_completion_list(core[modulo])
        else:
            core=utils.load_json_packages_path("nodejs", "core.json")
            return utils.get_completion_list(core.keys())
        