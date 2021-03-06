import sublime, sublime_plugin

class UnicodeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("replace", {"old":"ó", "new":"\\u00f3"})
        view.run_command("replace", {"old":"Ó", "new":"\\u00D3"})
        view.run_command("replace", {"old":"í", "new":"\\u00ED"})
        view.run_command("replace", {"old":"Í", "new":"\\u00CD"})
        view.run_command("replace", {"old":"ñ", "new":"\\u00F1"})
        view.run_command("replace", {"old":"Ñ", "new":"\\u00D1"})
        view.run_command("replace", {"old":"é", "new":"\\u00E9"})
        view.run_command("replace", {"old":"É", "new":"\\u00C9"})
        view.run_command("replace", {"old":"á", "new":"\\u00E1"})
        view.run_command("replace", {"old":"Á", "new":"\\u00C1"})
        view.run_command("replace", {"old":"ú", "new":"\\u00FA"})
        view.run_command("replace", {"old":"Ú", "new":"\\u00DA"})

class ReverseToNormalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window=sublime.active_window()
        view=window.active_view()
        view.run_command("replace", {"old":"\\u00F3", "new":"ó"})
        view.run_command("replace", {"old":"\\u00f3", "new":"ó"})
        view.run_command("replace", {"old":"\\u00D3", "new":"Ó"})
        view.run_command("replace", {"old":"\\u00d3", "new":"Ó"})
        view.run_command("replace", {"old":"\\u00ED", "new":"í"})
        view.run_command("replace", {"old":"\\u00ed", "new":"í"})
        view.run_command("replace", {"old":"\\u00CD", "new":"Í"})
        view.run_command("replace", {"old":"\\u00cd", "new":"Í"})
        view.run_command("replace", {"old":"\\u00F1", "new":"ñ"})
        view.run_command("replace", {"old":"\\u00f1", "new":"ñ"})
        view.run_command("replace", {"old":"\\u00D1", "new":"Ñ"})
        view.run_command("replace", {"old":"\\u00d1", "new":"Ñ"})
        view.run_command("replace", {"old":"\\u00E9", "new":"é"})
        view.run_command("replace", {"old":"\\u00e9", "new":"é"})
        view.run_command("replace", {"old":"\\u00C9", "new":"É"})
        view.run_command("replace", {"old":"\\u00c9", "new":"É"})
        view.run_command("replace", {"old":"\\u00E1", "new":"á"})
        view.run_command("replace", {"old":"\\u00e1", "new":"á"})
        view.run_command("replace", {"old":"\\u00C1", "new":"Á"})
        view.run_command("replace", {"old":"\\u00c1", "new":"Á"})
        view.run_command("replace", {"old":"\\u00FA", "new":"ú"})
        view.run_command("replace", {"old":"\\u00fa", "new":"ú"})
        view.run_command("replace", {"old":"\\u00DA", "new":"Ú"})
        view.run_command("replace", {"old":"\\u00da", "new":"Ú"})
