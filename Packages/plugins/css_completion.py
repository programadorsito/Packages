import sublime_plugin
import sublime
import utils

class CssCompletionListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        lang=utils.get_language()
#        print(self.get_line_until_sel())

    def get_line_until_sel(self):
        window=sublime.active_window()
        view=window.active_view()
        return view.substr(sublime.Region(view.line(view.sel()[0]).a, view.sel()[0].b))

