import shutil
import re
import os.path
import os
import sublime
import sublime_plugin
import utils

class RecursosHtml:
	def __init__(self, path, tipo):
		self.tipo=tipo
		self.pathJs=sublime.packages_path()+os.sep+"html5"+os.sep+self.tipo
		self.path=path
		self.window=sublime.active_window()
		self.view=self.window.active_view()

	def insertar(self, index=None):
		if index==None:
			self.librerias=[]
			self.tomarLibrerias(self.pathJs)
			self.lista=[]
			for libreria in self.librerias:
				self.lista.append([libreria.replace(self.pathJs, ""), libreria])
			self.window.run_command("hide_auto_complete")
			self.window.show_quick_panel(self.lista, self.insertar)
		elif index!=-1:
			pathSrc=self.librerias[index]
			pathDts=self.path+os.sep+self.tipo+self.lista[index][0]
			path=pathDts
			path=path[:path.rfind("/")] if path.find("/")!=-1 else path[:path.rfind("\\")]
			try:os.makedirs(path)
			except:pass
			shutil.copyfile(pathSrc,pathDts)
			self.view.run_command("insert", {"characters":self.tipo+self.lista[index][0].replace("\\", "/")})

	def tomarLibrerias(self, path):
		if os.path.isdir(path):
			for p in os.listdir(path):
				self.tomarLibrerias(path+os.sep+p)
		else:self.librerias.append(path)

class CompletionsHtmlListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		window=sublime.active_window()
		view=window.active_view()
		self.clases=set()
		lang=utils.get_language()
		if lang=="html" or lang=="php":
			punto=view.sel()[0].a
			linea=view.substr(sublime.Region(view.line(punto).a, punto)).replace('"', "'")
			linea=linea[:linea.rfind("'")].strip()
			print("la linea es :"+linea)
			if linea.endswith("class="):
				print("en compass")
				cssFiles=utils.get_files({"ext":"css"})
				self.clases=[]
				for cssFile in cssFiles:
					texto=open(cssFile).read()
					cssClases=re.findall("\.(?P<clase>[a-z][-\w]*)\s+", texto)
					self.clases=self.clases + cssClases
				self.clases=list(set(self.clases))
				self.clases=[[clase + "\t(CSS)", clase] for clase in self.clases]

				return list(self.clases)

			linea=view.substr(sublime.Region(view.line(punto).a, punto)).replace('"', "'").strip()
			if linea.endswith("src='") and linea.startswith("<script"):
				path=view.file_name()
				path=path[:path.rfind("/")] if path.find("/")!=-1 else path[:path.rfind("\\")]
				RecursosHtml(path, "js").insertar()
			elif linea.endswith("href='") and linea.startswith("<link "):
				path=view.file_name()
				path=path[:path.rfind("/")] if path.find("/")!=-1 else path[:path.rfind("\\")]
				RecursosHtml(path, "css").insertar()

	def listaClasesCss(self, csss, path):
		for css in csss:
			if css.startswith("http://") or css.startswith("https://"):return
			css=path+os.sep+css 
			texto=open(css).read()
			sep="/" if css.find("/")!=-1 else "\\"
			

