import os
import os.path
import sublime
import sublime_plugin
import webbrowser

class HelpBrowserCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		self.words=texto
		self.determinarSitio()
		if not self.url:
			sublime.status_message("no hay un sitio en el que buscar")
			return
		webbrowser.open_new_tab(self.url)

	def determinarSitio(self):
		window=sublime.active_window()
		view=window.active_view()
		filename=view.file_name()
		if filename:filename = os.path.basename(filename)
		scope=view.scope_name(view.sel()[0].a)
		if filename == "pom.xml":
			sublime.status_message("Ayuda maven")
			self.url="https://www.google.com.co/?gfe_rd=cr&ei=cjaTVJr0KpOw8wfQs4GoCA&gws_rd=ssl#q=site:http:%2F%2Fmaven.apache.org%2F+"+self.words.replace(" ", "+")
		elif scope.startswith("source.python"):
			self.url="https://docs.python.org/2/search.html?q="+self.words.replace(" ", "+")
		elif scope.startswith("source.java"):
			self.url="https://www.google.com.co/?gws_rd=ssl#q=site%3Ahttp%3A%2F%2Fdocs.oracle.com%2Fjavase%2F7%2Fdocs%2Fapi%2F+"+self.words.replace(" ", "+")
		elif scope.startswith("text.jsf "):
			self.url="https://www.google.com.co/?gws_rd=ssl#q=site:jsftoolbox.com+"+self.words.replace(" ", "+")
		elif scope.startswith("source.css"):
			self.url="https://www.google.com.co/?gws_rd=ssl#q=site+:+www.w3schools.com%2Fcss+"+self.words.replace(" ", "+")
		elif scope.startswith("source.ruby"):
			self.url="https://www.google.com.co/?gws_rd=ssl#q=site%3A+ruby-doc.org%2Fcore-2.1.3%2F+"+self.words.replace(" ", "+")
		elif scope.startswith("source.nodejs"):
			self.url="https://www.google.com.co/?gfe_rd=cr&ei=FGHVVMHMBpCw8we1qIHQDQ&gws_rd=ssl#q=site:http:%2F%2Fnodejs.org%2Fapi%2F+"+self.words.replace(" ", "+")
		elif scope.find(".php ")!=-1:
			self.url="http://php.net/manual-lookup.php?pattern="+self.words.replace(" ", "+")


					#https://www.google.com.co/?gws_rd=ssl#q=site:%(site)s+%(words)s"%{"site":self.sitio, "words":texto.replace(" ", "+")})
		
class HelpBootstrapCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="https://www.google.com.co/?gws_rd=ssl#q=site:getbootstrap.com+"+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)

class HelpStackoverflowCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="http://stackoverflow.com/search?q="+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)

class HelpJavaeeTutorialCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="https://www.google.com.co/?gws_rd=ssl#q=site%3A+http%3A%2F%2Fdocs.oracle.com%2Fjavaee%2F7%2Ftutorial%2Fdoc%2F+"+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)

class HelpJavaeeApiCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="https://www.google.com.co/?gws_rd=ssl#q=site%3Adocs.oracle.com%2Fjavaee%2F7%2Fapi%2F+"+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)

class HelpPrimefacesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="https://www.google.com.co/?gws_rd=ssl#q=site:primefaces.org+"+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)

class HelpPrimefacesApiCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="https://www.google.com.co/?gws_rd=ssl#q=site:primefaces.org%2Fdocs%2Fapi%2F5.0%2F+"+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)	

class HelpSublimeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		url="https://www.sublimetext.com/docs/3/api_reference.html"
		webbrowser.open_new_tab(url)	

class HelpJqueryCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.url=""
		window=sublime.active_window()
		window.show_input_panel("termino de busqueda", "", self.buscar, None, None)
	
	def buscar(self, texto):
		url="http://api.jquery.com/?s="+texto.replace(" ", "+")
		webbrowser.open_new_tab(url)