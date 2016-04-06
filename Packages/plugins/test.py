import sublime
import sublime_plugin

class testCommand(sublime_plugin.TextCommand):
	def run(view, edit):
		print("test el comando")