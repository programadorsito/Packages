import sublime
import sublime_plugin
import os
import re
from subprocess import Popen, PIPE, call
import utils

class CompilarCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view = sublime.active_window().active_view()
		view=self.view
		lang = utils.get_language()
		archivo = self.extraerArchivo(view.file_name(), lang)
		proceso=None
		salida=1
		puntos=[]
		errores=[]	
		os.chdir(archivo["ruta"])
		patron=None
		patronNumerico=re.compile("\d+")
		if lang=="java" or lang=="c":
			patron=re.compile(":\d+: error:")
		if lang=="java":
			comando="javac %(nombreCompleto)s"%archivo
		elif lang=="c":
			comando="gcc %(nombreCompleto)s -o %(nombre)s"%archivo
		elif lang=="scala":
			comando="scalac %(nombreCompleto)s"%archivo
			patron=re.compile("\(\d+\): Error:")
		elif lang=="cs":
			salida=0
			comando="csc %(nombreCompleto)s"%archivo
			patron=re.compile("\(\d+,\d+\): error")
		elif lang=="d":
			comando="dmd %(nombreCompleto)s"%archivo
			patron=re.compile("\(\d+\): Error:")
		else:
			sublime.status_message("no tiene compilacion")
			return
		
		print(comando)
		proceso=Popen(comando, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
		error=proceso.communicate()[salida]
		if error:	
			listaErrores=error.decode("utf-8").splitlines()
			for e in listaErrores:
				e=e.strip()
				errorl=patron.search(e)
				if errorl:
					errorl=errorl.group()
					punto=patronNumerico.search(errorl).group().replace(":", "").replace(",","")
					puntos.append(punto)
					errores.append(punto+":"+e[e.rfind(":")+1:])
		
		if errores:
			self.marcarErrores(puntos)
			f=open(sublime.packages_path()+os.sep+"errores.txt", "w")
			for p in errores:f.write(p+"\n")
			f.close()
			view.run_command("buscar_errores")
		if proceso.returncode==0:
			self.view.erase_regions("errores")
			sublime.status_message("-----BIEN-----")
		else:
			sublime.status_message("-----MAL-----")

	def marcarErrores(self, filas):
		lineas=self.view.split_by_newlines(sublime.Region(0, self.view.size()))
		regiones=[]
		for l in filas:regiones.append(lineas[int(l)-1])
		self.view.add_regions("errores", regiones, "comment", "bookmark", sublime.DRAW_OUTLINED)


	def extraerArchivo(self, path, lang):
		archivo={}
		view=sublime.active_window().active_view()
		if not path:
			if lang=="java":path=sublime.packages_path()+os.sep+"app.java"
			elif lang=="d":path=sublime.packages_path()+os.sep+"app.d"
			elif lang=="scala":path=sublime.packages_path()+os.sep+"app.d"
			elif lang=="c":path=sublime.packages_path()+os.sep+"app.c"
			elif lang=="cs":path=sublime.packages_path()+os.sep+"app.cs"
			print(path)
			fil=open(path, "w")
			fil.write(self.view.substr(sublime.Region(0, self.view.size())))
			fil.close()
		else:self.view.run_command("save")
		path=path.strip()
		sep="\\"
		if path.find("/")!=-1:sep="/"
		archivo["nombreCompleto"]=path[path.rfind(sep)+1:]
		archivo["ruta"]=path[:path.rfind(sep)]
		if(archivo["nombreCompleto"].find(".")!=-1):
			archivo["nombre"]=archivo["nombreCompleto"][:archivo["nombreCompleto"].find(".")]
			archivo["extension"]=archivo["nombreCompleto"][archivo["nombreCompleto"].find(".")+1:]
		else:
			archivo["nombre"]=archivo["nombreCompleto"]
		return archivo


