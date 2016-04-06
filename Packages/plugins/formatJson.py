import sublime_plugin
import sublime
import utils

class FormatJsonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        utils.set_text(sublime.encode_value(sublime.decode_value(utils.get_text()), True))