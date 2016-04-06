import os.path
import sublime
import os
import sublime_plugin

class HistoryFilesListener(sublime_plugin.EventListener):
	def on_close(self, view):
		window=sublime.active_window()
		self.ruta=os.path.join(sublime.packages_path(),"Plugins","historyFiles.json")
		self.cargarArchivos()
		filename=view.file_name()
		if not filename:return
		if filename in self.archivos["archivos"]:self.archivos["archivos"].remove(filename)
		self.archivos["archivos"].append(filename)

		folder=window.folders()
		if folder:folder=folder[0]
		if not folder:return
		if folder in self.archivos["carpetas"]:self.archivos["carpetas"].remove(folder)
		self.archivos["carpetas"].append(folder)
		
		self.guardarArchivos()

	def cargarArchivos(self):
		self.archivos=sublime.decode_value(open(self.ruta).read())
		if not self.archivos:self.archivos={"archivos":[], "carpetas":[]}
		if self.archivos.get("archivos")==None:self.archivos["archivos"]=[]
		if self.archivos.get("carpetas")==None:self.archivos["carpetas"]=[]


	def guardarArchivos(self):
		archivo=open(self.ruta, "w")
		if len(self.archivos["archivos"])>500:
			lista=self.archivos["archivos"]
			lista=list(reversed(list(reversed(lista))[:250]))
			self.archivos["archivos"]=lista

		if len(self.archivos["carpetas"])>500:
			lista=self.archivos["carpetas"]
			lista=list(reversed(list(reversed(lista))[:250]))
			self.archivos["carpetas"]=lista

		archivo.write(sublime.encode_value(self.archivos, True))
		archivo.close()


class HistoryFilesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.ruta=sublime.packages_path()+os.sep+"Plugins"+os.sep+"historyFiles.json"
		window=sublime.active_window()
		self.archivos=sublime.decode_value(open(self.ruta).read())
		if not self.archivos:return
		self.lista=[]
		self.archivos["archivos"]=list(reversed(self.archivos["archivos"]))
		for path in self.archivos["archivos"]:
			if not os.path.exists(path):continue
			if path.find("/")!=-1:
				self.lista.append([path[path.rfind("/")+1:], path])
			else:
				self.lista.append([path[path.rfind("\\")+1:], path])
		window.show_quick_panel(self.lista, self.seleccion)

	def seleccion(self, indice):
		if indice==-1:return
		window=sublime.active_window()
		window.open_file(self.lista[indice][1])

class HistoryFoldersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.ruta=sublime.packages_path()+os.sep+"Plugins"+os.sep+"historyFiles.json"
		self.window=window=sublime.active_window()
		self.archivos=sublime.decode_value(open(self.ruta).read())
		if not self.archivos:return
		self.lista=[]
		self.archivos["carpetas"]=list(reversed(self.archivos["carpetas"]))
		for path in self.archivos["carpetas"]:
			if not os.path.exists(path):continue
			self.lista.append([os.path.basename(path), path])
		window.show_quick_panel(self.lista, self.seleccion)

	def seleccion(self, indice):
		if indice==-1:return
		self.window.run_command("side_bar_open_in_new_window",{"paths": [self.lista[indice][1]+os.sep]})

