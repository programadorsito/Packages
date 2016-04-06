import os.path
import re
import subprocess
import os
import sublime
import sublime_plugin

class StylusCompileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		Stylus().compile()

class StylusCompressCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		Stylus().compress()

class StylusWatchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		Stylus().watch()

class RutasStylus:
	def rutaAtributos():
		pathStylus=os.path.join(sublime.packages_path(), "stylus", "stylus.json")
		RutasStylus.verificarRuta(pathStylus)
		return pathStylus

	def verificarRuta(ruta):
		if not os.path.exists(ruta):
			open(ruta, "w").close()

class ArchivoStylus:
	def cargar():
		d=sublime.decode_value(open(RutasStylus.rutaAtributos()).read())
		if d==None:
			d={"atributos":{}, "etiquetas":[]}
		return d

	def allEtiquetas():
		return ArchivoStylus.cargar()["etiquetas"]
	
	def allAtributos():
		return list(ArchivoStylus.cargar()["atributos"].keys())


	def allValores(etiqueta):
		d=ArchivoStylus.cargar()["atributos"]
		if d.get(etiqueta):
			return d[etiqueta]

	def guardar(d):
		open(RutasStylus.rutaAtributos(), "w").write(sublime.encode_value(d, True))

	def agregar(etiquetas, atributos):
		d=ArchivoStylus.cargar()
		d["etiquetas"]=list(set(d["etiquetas"]) | set(etiquetas))
		for atributo in atributos:
			if not d["atributos"].get(atributo):d["atributos"][atributo]=[]
			d["atributos"][atributo]=list(set(d["atributos"][atributo])|atributos[atributo])
		ArchivoStylus.guardar(d)

class Stylus:
	def __init__(self):
		self.filename=sublime.active_window().active_view().file_name()
		if self.filename:
			os.chdir(os.path.dirname(self.filename))
	
	def compile(self):
		if self.filename:
			self.ejecutar("stylus %s"%os.path.basename(self.filename))

	def compress(self):
		if self.filename:
			self.ejecutar("stylus -c %s"%os.path.basename(self.filename))

	def watch(self):
		if self.filename:
			self.ejecutar("stylus -w %s"%os.path.basename(self.filename))

	def comando(self, comando):
		return comando if sublime.platform()=="windows" else "gnome-terminal -x bash -c '%s'"%(comando)

	def ejecutar(self, comando, shell=True):
		proceso=subprocess.Popen(self.comando(comando), shell=shell, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		if proceso.communicate()[1]:
			error=proceso.communicate()[1].decode("utf-8")
			sublime.status_message("MAL "+error)
			print(error)
		else:
			salida=proceso.communicate()[0].decode("utf-8")
			sublime.status_message("BIEN"+salida)
			return salida

class StylusListener(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if not view.scope_name(0).startswith("source.stylus "):return
		punto=view.sel()[0].a
		linea=view.substr(sublime.Region(view.line(punto).a, punto))
		if re.match("^[\w]*$", linea):
			return [(e+"\t•", e) for e in ArchivoStylus.allEtiquetas()]
		elif re.match("^\s+[\w-]*$", linea):
			return [(a+"\t•", a) for a in ArchivoStylus.allAtributos()]
		elif re.match("^\s+[\w-]+\s+[\w-]*$", linea):
			atributo=re.findall("^\s+([\w-]+)\s+[\w-]*$", linea)[0]
			return [(v+"\t•", v) for v in ArchivoStylus.allValores(atributo)]

	def on_pre_save(self, view):
		if not view.scope_name(0).startswith("source.stylus "):return
		texto=view.substr(sublime.Region(0, view.size()))
		etiquetas=re.findall("\n([\w]+)\n", texto)
		atributos=re.findall("\s+([\w-]+) ([\w -]+)", texto)
		variables=re.findall("([\w$]+)\s*=.", texto)
		a={}
		for atributo in atributos:
			valor=atributo[1]
			if valor in variables:continue
			atributo=atributo[0]
			if not a.get(atributo):a[atributo]=set()
			a[atributo].add(valor)
		ArchivoStylus.agregar(etiquetas, a)
		view.run_command("stylus_compile")